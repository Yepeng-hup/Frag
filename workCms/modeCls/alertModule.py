from workCms.databases.mysql_db import cursor


class Alert(object):
    alert = list()

    def todayDateResult(self):
        cursor.execute("select server_date from server order by server_id desc limit 1")
        rel = cursor.fetchall()
        for i in rel:
            for _, v in i.items():
                return v

    def allAlertResult(self):
        cursor.execute("select server_policeNum from server")
        rel = cursor.fetchall()
        relNum = 0
        for i in rel:
            for _, v in i.items():
                relNum += int(v)
        return relNum

    def alldayAlertResult(self, date):
        cursor.execute("select server_policeNum from server WHERE server_date=%(date)s", {"date": date})
        rel = cursor.fetchall()
        alertNum = 0
        for i in rel:
            for _, v in i.items():
                alertNum += int(v)
        return alertNum

    def alertScreen(self):
        cursor.execute("select server_info from server")
        rel = cursor.fetchall()
        for i in rel:
            for _, v in i.items():
                if '，' in v:
                    v = v.split('，')
                elif ',' in v:
                    v = v.split(',')
                elif '\r' in v:
                    v = v.split('\r')
                elif ' ' in v:
                    v = v.split(' ')
                else:
                    v = v.split('\n')
                self.alert.append(v)
        merge_alert_list = sum(self.alert, [])
        self.alert.clear()
        strList = list(set(merge_alert_list))
        strRel = list()
        numRel = list()
        for i in strList:
            num = merge_alert_list.count(i)
            strRel.append(i)
            numRel.append(num)
        merge_alert_list.clear()
        return strRel, numRel
