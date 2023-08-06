import requests
import datetime
from bs4 import BeautifulSoup

from pychara.exceptions import (LoginFailureException,
                                LoginRequireException,
                                HTTPConnectException,
                                HTMLParseException,
                                ApplyDisableException)

LOGIN = 'login'
LOGOUT = 'logout'

class Session():
    """ログインセッションを張るためのクラス
    """
    def __init__(self):
        self.cookies = None
        self.BASE_URL = 'https://akb48.chara-ani.com'
        self.LOGIN_URL = '{}/login.aspx'.format(self.BASE_URL)
        self.LOGOUT_URL = '{}/logout.aspx'.format(self.BASE_URL)
        self.APPLY_URL = '{}/akb_history.aspx'.format(self.BASE_URL)
        self.PURCHASE_URL = '{}/purchase_history.aspx'.format(self.BASE_URL)
        self.POST_URL = '{}/hall1/akbreserve.aspx'.format(self.BASE_URL)

    def _find_hidden(self, html):
        soup = BeautifulSoup(html, "html.parser")
        input_els = soup.find_all("input")
        hidden_data = {}
        for input_el in input_els:
            _type = input_el.get("type")
            if _type in "hidden":
                hidden_data[input_el.get("name")] = input_el.get("value")

        return hidden_data

    def login(self, username, password):
        """ログイン処理を行う関数

        Args:
            username (str): ユーザー名
            password (str): パスワード

        Returns:
            str: ログインに成功したユーザー名

        Raises:
            pychara.exceptions.LoginfailureException
            pychara.exceptions.HTTPConnectException
        Examples:
            >>> login('username', 'password')
            'username'
        """
        pre = requests.get(self.LOGIN_URL)
        self.cookies = pre.cookies
        postdata = self._find_hidden(pre.text)
        postdata['ScriptManager1'] = 'ScriptManager1%7CbtnLogin'
        postdata['txID'] = username
        postdata['txPASSWORD'] = password
        postdata['btnLogin.x'] = '173'
        postdata['btnLogin.y'] = '30'
        res = requests.post(self.LOGIN_URL,
                            data=postdata,
                            cookies=self.cookies)
        soup = BeautifulSoup(res.text, "html.parser")
        username_el = soup.find(attrs={"id": "lblUserName"})
        if username_el is None \
           and res.status_code == 200:
            raise LoginFailureException('Invalid username or password')
        elif res.status_code != 200:
            msg = 'Bad HTTP Status Code returnd {}'.format(res.status_code)
            raise HTTPConnectException(msg)
        self.displayName = username_el.text
        return self.displayName

    def get(self, url, params=None):
        """セッションを保持しながらGETリクエストを投げる関数

        Args:
            url (str): URL
            params (dict): GETパラメータ

        Returns:
            requests.models.Response: レスポンス
        """

        if params is None:
            params = {}

        assert isinstance(params, dict)

        res = requests.get(url,
                           params=params,
                           cookies=self.cookies)
        return res

    def post(self, url, data=None):
        """セッションを保持しながらPOSTリクエストを投げる関数

        Args:
            url (str): URL
            data (dict): POSTパラメータ

        Returns:
            requests.models.Response: レスポンス
        """
        if data is None:
            data = {}

        assert isinstance(data, dict)

        res = requests.get(url,
                           data=data,
                           cookies=self.cookies)
        return res


    def status(self):
        """ログインチェックを行う関数

        Returns:
            str: pyfortune.session.LOGINかpyfortune.session.LOGOUTが返される

        Examples:
            >>> status()
            'login'
        """
        res = requests.get(self.BASE_URL, cookies=self.cookies)
        soup = BeautifulSoup(res.text, "html.parser")
        username_el = soup.find(attrs={"id": "lblUserName"})
        if username_el is None:
            return LOGOUT
        return LOGIN

    def reservable_status(self):
        """
        Returns:
            bool: 抽選申し込み可能ならTrue、そうでなければFalse

        Examles:
            >>> reserveable_status()
            True
        """
        res = requests.get(self.BASE_URL, cookies=self.cookies)
        soup = BeautifulSoup(res.text, "html.parser")
        main_btn_el = soup.find(attrs={"class": "main_btn01"})
        if main_btn_el is None:
            return False
        return True

    def fetch_apply_list(self, page=None):
        """抽選申し込み履歴の抽出

        Args:
            page (int): 申し込み履歴を抽出するpage番号、最初は1

        Returns:
            list: 申し込み情報の辞書のリスト

        Raises:
            pychara.exceptions.LoginRequireException
            pychara.exceptions.HTTPConnectException
            pychara.exceptions.HTMLParseException

        Examples:
            >>> fetch_apply_list()
        """

        if self.status() is LOGOUT:
            raise LoginRequireException('Require Login')

        if page is None:
            page = 1

        res = requests.get(self.APPLY_URL, cookies=self.cookies)
        #  2ページ目以降は1ページ目からリンクを踏む必要がある
        if page > 1:
            postdata = self._find_hidden(res.text)
            postdata['__EVENTARGUMENT'] = 'Page$%s' % page
            postdata['__EVENTTARGET'] = 'dgvList'
            res = requests.post(self.APPLY_URL,
                               cookies=self.cookies,
                               data=postdata)
        if res.status_code != 200:
            msg = 'Bad HTTP Status Code returnd {}'.format(res.status_code)
            raise HTTPConnectException(msg)
        soup = BeautifulSoup(res.text, 'html.parser')
        table_el = soup.find(id='dgvList')
        if table_el is None:
            raise HTMLParseException('table element not found')
        tr_els = table_el.findAll('tr')
        if len(tr_els) < 6:
            raise HTMLParseException('tr element not found')
        #  前3行と後ろ2行はナビゲーション等なので除外
        tr_els = tr_els[3:-2]
        apply_list = []
        for tr_el in tr_els:
            td_list = tr_el.findAll('td')
            if len(td_list) != 8:
                raise HTMLParseException('td element num is not 8')
            date = datetime.datetime.strptime(td_list[0].text, '%Y年%m月%d日')
            id = td_list[1].text
            name = td_list[2].text
            one_money = int(td_list[3].text[1:].replace(',', ''))
            num = int(td_list[4].text[:-1])
            total_money = int(td_list[5].text[1:].replace(',', ''))
            status = td_list[6].text
            status_code = -1
            if status == '当選':
                status_code = 0
            elif status == '落選':
                status_code = 1
            elif status == '抽選中':
                status_code = 2
            apply_list.append({'date': date,
                               'id': id,
                               'name': name,
                               'one_money': one_money,
                               'num': num,
                               'total_money': total_money,
                               'status': status,
                               'status_code': status_code})

        return apply_list

    def fetch_purchase_list(self, page=None):
        """購入履歴の抽出

        Args:
            page (int): 購入履歴を抽出するpage番号、最初は1 最大で4

        Returns:
            list: 申し込み情報の辞書のリスト

        Raises:
            pychara.exceptions.LoginRequireException
            pychara.exceptions.HTTPConnectException
            pychara.exceptions.HTMLParseException

        Examples:
            >>> fetch_purchase_list()
        """

        if self.status() is LOGOUT:
            raise LoginRequireException('Require Login')

        if page is None:
            page = 1

        res = requests.get(self.PURCHASE_URL, cookies=self.cookies)
        if res.status_code != 200:
            msg = 'Bad HTTP Status Code returnd {}'.format(res.status_code)
            raise HTTPConnectException(msg)
        #  2ページ目以降は1ページ目から順番にページを移動する必要がある
        for i in range(page - 1):
            postdata = self._find_hidden(res.text)
            postdata['__EVENTARGUMENT'] = ''
            postdata['__EVENTTARGET'] = 'lastLink'
            res = requests.post(self.PURCHASE_URL,
                                cookies=self.cookies,
                                data=postdata)
            if res.status_code != 200:
                msg = 'Bad HTTP Status Code returnd {}'.format(res.status_code)
                raise HTTPConnectException(msg)
        soup = BeautifulSoup(res.text, 'html.parser')
        table_els = soup.findAll('table', attrs={'class': 'purchase_table'})
        if table_els is None:
            raise HTMLParseException('table element not found')

        purchase_list = []
        for table_el in table_els:
            tr_els = table_el.findAll('tr')
            # 上4行が申し込み情報
            if len(tr_els) < 5:
                raise HTMLParseException('tr element num is not more 5 [%s]' % len(tr_els))

            date = datetime.datetime.strptime(tr_els[0].findAll('td')[1].text, '%Y/%m/%d %H:%M')
            id = tr_els[0].findAll('td')[3].text
            username = tr_els[1].find('td').text
            # 郵便番号の後にひとつだけ全角スペースがあるので半角スペースに変換する
            address = tr_els[2].text.strip().replace('　', ' ')

            details = []
            # 5行目から申し込み商品詳細
            for i in range(4, len(tr_els)):
                tr_el = tr_els[i]
                td_els = tr_el.findAll('td')
                if len(td_els) < 2:
                    raise HTMLParseException('tr element num is not more 5 [%s]' % len(tr_els))
                name = td_els[0].text
                num = int(td_els[1].text[:-1])
                details.append({'name': name, 'num': num})

            purchase_data = {'date': date,
                             'id': id,
                             'username': username,
                             'address': address,
                             'details': details}
            purchase_list.append(purchase_data)
        return purchase_list

    def fetch_apply_schedule(self):
        """申し込みスケジュールの取得

        Returns:
            list: 申し込みスケージュール情報の辞書のリスト

        Raises:
            pychara.exceptions.HTTPConnectException
            pychara.exceptions.HTMLParseException

        Examples:
            >>> fetch_apply_schedule()
            [{'title': '...', 'body': '...'}, {'title...]
        """
        res = requests.get(self.BASE_URL, cookies=self.cookies)
        if res.status_code != 200:
            msg = 'Bad HTTP Status Code returnd {}'.format(res.status_code)
            raise HTTPConnectException(msg)
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            contents_el = soup.findAll('div', attrs={'id': 'mainTopContents3_l'})[0]
            contents_el = contents_el.find('div', attrs={'class': 'accordion_block'})
            content_els = contents_el.findAll(['h3', 'p'])
            apply_schedule_list = []
            # h3とpを1セットにする、注釈でpが1つ余る
            i = 0
            while i < len(content_els):
                content_el = content_els[i]
                if content_el.name == 'h3':
                    h3_el = content_el
                    p_el = content_els[i+1]
                    title = h3_el.text
                    body = p_el.text
                    apply_schedule_list.append({'title': title,
                                                'body': body})
                    i = i + 2
                else:
                    i = i + 1
            return apply_schedule_list
        except Exception as error:
            raise HTMLParseException(error)


    def fetch_apply_enable(self):
        """申し込み受付中かどうかのチェック

        Returns:
            bool: 申し込み受付中ならTrue

        Raises:
            pychara.exceptions.HTTPConnectException
            pychara.exceptions.HTMLParseException

        Examples:
            >>> fetch_apply_enable()
            True
        """
        res = requests.get(self.BASE_URL, cookies=self.cookies)
        if res.status_code != 200:
            msg = 'Bad HTTP Status Code returnd {}'.format(res.status_code)
            raise HTTPConnectException(msg)
        soup = BeautifulSoup(res.text, 'html.parser')
        main_btn_el = soup.find('div', 'main_btn01')
        if main_btn_el is None:
            return False
        return True

    def fetch_apply_events(self):
        """申し込み可能な日程とグループのリストを取得

        Returns:
            list: 申し込み可能な日程とグループのリスト

        Raises:
            pychara.exceptions.HTTPConnectException
            pychara.exceptions.HTMLParseException
            pychara.exceptions.ApplyDisableException

        Examples:
            >>> fetch_apply_enables()
            [{'text': '...', 'value': '...'}, {'text...]
        """
        if not self.fetch_apply_enable():
            raise ApplyDisableException('Apply disable')
        res = requests.get(self.POST_URL, cookies=self.cookies)
        if res.status_code != 200:
            msg = 'Bad HTTP Status Code returnd {}'.format(res.status_code)
            raise HTTPConnectException(msg)
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            events_els = soup.find('select')
            options_els = events_els.findAll('option')
            apply_list =  [{'text': e.text, 'value': e.attrs['value']} for e in options_els]
            return apply_list
        except Exception as error:
            raise HTMLParseException(error)

