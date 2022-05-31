from enum import IntEnum
import re
from . import FormatExpr


def _acceptedFormat():
    d = 'd'
    m = 'm'
    y = 'y'
    s = '-'
    l1 = [m, d+m, m+d]
    l2 = l1 + [u+s+u for u in l1] + [d+s+d+m, m+d+s+d]
    l3 = [y+v for v in l2] + [v+y for v in l2]
    l4 = [y+u+s+y+u for u in l1] + [u+y+s+u+y for u in l1]
    return l2 + [y,y+s+y] + l3 + l4


class Date:
    """
    A day or range of days, months and/or years.
    Ranges are denoted by a dash or double dash.
    Months can be given as a full word or the three first letter (possibly followed by a dot)
    (e.g. 'January', 'jan'or 'jan.'). The case does not matter. Comas are ignored.

    With D for the day number, M for the month, Y for the year and - for a single or double dash,
    the following date strings are valid (spaces does not matter):
    M
    D M or M D
    U - U or D - D M or M D - D where U is one of the above
    and, with V one of the above combination:
    Y
    Y - Y
    Y V or V Y
    Y U - Y U or U Y - U Y
    """

    class _Type(IntEnum):
        DAY = 0         # Number from 1 to 31
        MONTH = 1       # Word w such that w is in _months, or _mon or w = v+'.' and v is in _mon (case insensitive)
        YEAR = 2        # Number betwenn 1000 and 2999
        DASH = 3        # '-' or '--'
        ORDINAL = 4     # 'st', 'nd', 'rd' or 'th'
        OTHER = 5       # Any other non-space non-coma character chain
    
    _months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    _mon = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    _max = [31,29,31,30,31,30,31,31,30,31,30,31]
    # all possible date formats. Generated with _acceptedFormat() above
    _acceptedFormat = ['m', 'dm', 'md', 
                       'm-m', 'dm-dm', 'md-md', 'd-dm', 'md-d', 
                       'y', 'y-y', 
                       'ym', 'ydm', 'ymd', 'ym-m', 'ydm-dm', 'ymd-md', 'yd-dm', 'ymd-d', 'my', 'dmy', 'mdy', 'm-my', 'dm-dmy', 'md-mdy', 'd-dmy', 'md-dy', 
                       'ym-ym', 'ydm-ydm', 'ymd-ymd', 'my-my', 'dmy-dmy', 'mdy-mdy']


    def __init__(self, str):
        s = str.replace(',', '').replace('~', ' ')       #remove comas and tilde
        if len(s.strip()) == 0:
            raise ValueError("Cannot build Date from an empty string.")
        self._day = None
        self._month = None
        self._year = None
        self._parse(s)

    def day(self):
        if self._day:
            if self._day[0] == self._day[1]:
                return self._day[0]
            else:
                return self._day
        else:
            return None

    def month(self):
        if self._month:
            if self._month[0] == self._month[1]:
                return self._months[self._month[0]]
            else:
                return [self._months[self._month[0]], self._months[self._month[1]]]
        else:
            return None

    def year(self):
        if self._year:
            if self._year[0] == self._year[1]:
                return self._year[0]
            else:
                return self._year
        else:
            return None

    def hasDayRange(self):
        return self._day and (self._day[0] != self._day[1] or self.hasMonthRange())

    def hasMonthRange(self):
        return self._month and (self._month[0] != self._month[1] or self.hasYearRange())

    def hasYearRange(self):
        return self._year and self._year[0] != self._year[1]

    def isRange(self):
        return self.hasDayRange() or self.hasMonthRange() or self.hasYearRange()

    def format(self, formatExpr):
        """ 
        Replace the placeholders in formatExpr with the relevant data.
        Placeholders can be:
          - for years: %Year%, %year%, %YEAR%, %Y%, %y%, %YY%, %YYYY%, %yy%, %yyyy%
          - for months: %Month%, %month%, %MONTH%, %Mon%, %mon%, %MON%, %Mon.%, %mon.%, %MON.%, %mm%, %MM%, %m%, %M%
          - for days: %Day%, %day%, 'DAY%, %D%, %d%, %dd%, %DD%, %Dayth%, %dayth%, %DAYTH%, %Dth%, %DTH%, %dth%
        or any of the above with 1 or 2 appended (e.g %month2%)
        %Year%, %year%, %YEAR%, %Y%, %y%, %YYYY% or %yyyy% will be replaced by the year.
        %YY% or %yy% will be replaced by the two last digits of the year.
        %Month% will be replaced with the month name in full, with first letter in upper case and other letters in lower case.
        %month% will be replaced with the month name in full, with all letters in lower case.
        %MONTH% will be replaced with the month name in full, with all letters in upper case.
        %Mon% (resp. %Mon.%) will be replaced with the abbreviation of the month with first letter in upper case, and without (resp. with) terminal dot.
        %mon% (resp. %mon.%) will be replaced with the abbreviation of the month with all letters in lower case, and without (resp. with) terminal dot.
        %MON% (resp. %MON.%) will be replaced with the abbreviation of the month with all letters in upper case, and without (resp. with) terminal dot.
        %mm% or %MM% will be replaced by the numeral version of the month with 2 digits (eg 04 for April).
        %m% or %M% will be replaced by the numeral version of the month with minimum number of digits (eg 4 for April and 11 for November)
        %Day%, %day%, $DAY%, %D% and %d% will be replaced by the day number.
        %DD% or %dd% will be replaced by the day number with two digits.
        %Dayth%, %dayth%, $DAYTH%, %Dth%, %DTH%, %dth% will be replaced by the ordinal number for the day.
        
        For a single date, %placeholder% and %placeholder1% are equivalent, and %placeholder2% is replace by ''.
        For a range date:
         - %placeholder1% corresponds to the start date while %placeholder2% corresponds to the stop date. 
         - The first time the corresponding data (year, month or day) is accessed %placeholder% will be replaced by the data of the start date. 
           The second time, it will be replaced by the data of the end date, if this data is different from that of the first year, and by '' otherwise.
           In this context, two months are considered different if they are different or the years are different, and days are different if any data is 
           different. For example in the range 12 March 2019 - 12 May 2019, the years are the same, the months are different, and so are the days.
        """

        ph = ['Year', 'year', 'YEAR', 'Y', 'y', 'YY', 'YYYY', 'yy', 'yyyy', 
              'Month', 'month', 'MONTH', 'Mon', 'mon', 'MON', 'Mon.', 'mon.', 'MON.', 'mm', 'MM', 'm', 'M', 
              'Day', 'day', 'DAY', 'D', 'd', 'dd', 'DD', 'Dayth', 'dayth', 'DAYTH', 'Dth', 'DTH', 'dth']
        placeholders = ph + [p+'1' for p in ph] + [p+'2' for p in ph]
        f = FormatExpr.FormatExpr(placeholders, formatExpr)
        l = f.placeholderList()
        replacements = []
        ymd = [1, 1, 1]
        for e in l:
            el = e.lower()
            if 'y' in el and not 'd' in el:
                replacements.append(self._formatYear(e,ymd[0]))
                ymd[0] += 1
            elif 'm' in el:
                replacements.append(self._formatMonth(e,ymd[1]))
                ymd[1] += 1
            else:
                replacements.append(self._formatDay(e,ymd[2]))
                ymd[2] += 1

        return f.reduce(replacements).strip()


    def _formatYear(self, formatExpr, n=1):
        def format(i, formatExpr, ignoreDuplicate = False):
            if self._year:
                if ignoreDuplicate and not self.hasYearRange():
                    return ''
                year = self._year[i-1]
            else:
                return ''
            if formatExpr in ['year', 'y', 'yyyy']:
                return str(year)
            elif formatExpr == 'yy':
                return '{:02d}'.format(year%100)
            else:
                raise ValueError('Incorrect formating string: ' + formatExpr)

        fe = formatExpr.lower()
        if self.isRange():
            if fe in ['year', 'y', 'yy', 'yyyy']:
                if n == 1:
                    return format(1, fe)
                elif n == 2:
                    return format(2, fe, True)
                else:
                    return ''
            if fe in ['year1', 'y1', 'yy1', 'yyyy1']:
                return format(1, fe[0:-1])
            if fe in ['year2', 'y2', 'yy2', 'yyyy2']:
                return format(2, fe[0:-1])
            raise ValueError('Incorrect formating string: ' + formatExpr)
        else:
            if fe in ['year', 'y', 'yy', 'yyyy']:
                return format(1, fe)
            if fe in ['year1', 'y1', 'yy1', 'yyyy1']:
                return format(1, fe[0:-1])
            if fe in ['year2', 'y2', 'yy2', 'yyyy2']:
                return ''
            raise ValueError('Incorrect formating string: ' + formatExpr)

    def _formatMonth(self, formatExpr, n=1):
        def format(i, formatExpr, ignoreDuplicate = False):
            if self._month:
                if ignoreDuplicate and not self.hasMonthRange():
                    return ''
                month = self._month[i-1]
            else:
                return ''
            if formatExpr == 'Month':
                return self._months[month]
            if formatExpr == 'month':
                return self._months[month].lower()
            if formatExpr == 'MONTH':
                return self._months[month].upper()
            if formatExpr == 'Mon':
                return self._mon[month][0].upper() + self._mon[month][1:]
            if formatExpr == 'mon':
                return self._mon[month].lower()
            if formatExpr == 'MON':
                return self._mon[month].upper()
            if formatExpr == 'Mon.':
                return self._mon[month][0].upper() + self._mon[month][1:]+'.'
            if formatExpr == 'mon.':
                return self._mon[month].lower()+'.'
            if formatExpr == 'MON.':
                return self._mon[month].upper()+'.'
            if formatExpr == 'mm':
                return '{:02d}'.format(month+1)
            if formatExpr == 'MM':
                return '{:02d}'.format(month+1)
            if formatExpr == 'm':
                return str(month+1)
            if formatExpr == 'M':
                return str(month+1)
            else:
                raise ValueError('Incorrect formating string: ' + formatExpr)

        if self.isRange():
            if formatExpr[-1] == '1':
                return format(1, formatExpr[0:-1])
            elif formatExpr[-1] == '2':
                return format(2, formatExpr[0:-1])
            else:
                if n == 1:
                    return format(1, formatExpr)
                elif n == 2:
                    return format(2, formatExpr, True)
                else:
                    return ''
        else:
            if formatExpr[-1] == '1':
                return format(1, formatExpr[0:-1])
            elif formatExpr[-1] == '2':
                return ''
            else:
                return format(1, formatExpr)

    def _formatDay(self, formatExpr, n=1):
        #%Day%, %day%, $DAY%, %D% and %d% will be replaced by the day number.
        #%DD% or %dd% will be replaced by the day number with two digits.
        #%Dayth%, %dayth%, $DAYTH%, %Dth%, %DTH%, %dth% will be replaced by the ordinal number for the day.
        def format(i, fe, ignoreDuplicate = False):
            if self._day:
                if ignoreDuplicate and not self.hasDayRange():
                    return ''
                day = self._day[i-1]
            else:
                return ''
            if fe.lower() == 'day' or fe.lower() == 'd':
                return str(day)
            if fe.lower() == 'dd':
                return '{:02d}'.format(day)
            if fe.lower() == 'dayth' or fe.lower() == 'dth':
                return Date._makeOrdinal(day)
            else:
                raise ValueError('Incorrect formating string: ' + fe)

        if self.isRange():
            if formatExpr[-1] == '1':
                return format(1, formatExpr[0:-1])
            elif formatExpr[-1] == '2':
                return format(2, formatExpr[0:-1])
            else:
                if n == 1:
                    return format(1, formatExpr)
                elif n == 2:
                    return format(2, formatExpr, True)
                else:
                    return ''
        else:
            if formatExpr[-1] == '1':
                return format(1, formatExpr[0:-1])
            elif formatExpr[-1] == '2':
                return ''
            else:
                return format(1, formatExpr)

    def _parse(self, str):
        s = re.findall('[a-z]+\.?|\d+|\-{1,2}|\S+',str.lower())  #find all words (possibly finishing by a dot), numbers and - or --
        types = [Date._getType(e) for e in s]
        if Date._Type.OTHER in types:
            raise ValueError('Date string contains unknown words or characters: ' + s[types.index(Date._Type.OTHER)])

        # compute the format of the input and check its validity
        chars = ['d','m','y', '-', '']
        sig = ''.join([chars[i] for i in types])
        if not sig in self._acceptedFormat:
            raise ValueError('Invalid date string: the format' + sig + ' is not accepted.')
        
        # Filling the _day, _month and _year fields
        for i in range(0,len(types)):
            if types[i] == Date._Type.DAY:
                self._addDay(int(s[i]))
            elif types[i] == Date._Type.MONTH:
                sm = s[i]    # string of the month
                self._addMonth(self._mon.index(sm[0:3])) # add the number of the month
            elif types[i] == Date._Type.YEAR:
                self._addYear(int(s[i]))

        # Check days validity (does not take leap or non-leap years into account)
        if self._day:
            for i in [0,1]:
                if self._day[i] > self._max[self._month[i]]:
                    raise ValueError('A day has a value greater than the maximum for this month')

        # Check the validity of the range (if any)
        def eq(x):
            return x[0] == x[1] if x else True
        def lower(x):
            return x[0] < x[1] if x else False
        ordered = lower(self._year) \
               or eq(self._year) and (   lower(self._month) \
                                      or eq(self._month) and (   lower(self._day)
                                                              or eq(self._day)))
        if not ordered:
            raise ValueError('Date range values are not correctly ordered')


    def _addDay(self, day):
        if self._day:
            self._day[1] = day
        else:
            self._day = [day,day]

    def _addMonth(self, month):
        if self._month:
            self._month[1] = month
        else:
            self._month = [month,month]

    def _addYear(self, year):
        if self._year:
            self._year[1] = year
        else:
            self._year = [year,year]

 #   def _format(self, formatExpr, first=True):
 #       for years: %Year, %year, %YEAR, %Y, %y, %YY, %YYYY, %yy, %yyyy
 #         - for months: %Month, %month, %MONTH, %M, %m, %M., %m., %mm, %MM, 
 #         - for days: %Day, %day, $DAY, %D, %d, %dd, %DD, %Dayth, %dayth, $DAYTH, %Dth, %DTH, %dth

    @staticmethod
    def _makeOrdinal(n):
        """ Return a string representing the ordinal number corresponding to n"""
        l = n%10
        ll = n%100
        if l==1 and ll!=11:
            return str(n)+'st'
        if l==2 and ll!=12:
            return str(n)+'nd'
        if l==3 and ll!=13:
            return str(n)+'rd'
        return str(n)+'th'

    @staticmethod
    def _getType(string):
        """ Determine the type of string """
        if string=='-' or string=='--':
            return Date._Type.DASH
        if string=='st' or string=='nd' or string=='rd' or string=='th':
            return Date._Type.ORDINAL
        g = re.search('^[0-3]?[0-9]$',string)   #match a day number
        if g:
            d = int(g[0])
            if d>0 and d <=31:
                return Date._Type.DAY
            else:
                return Date._Type.OTHER
        if string in [m.lower() for m in Date._months] or string in Date._mon or (string[3]=='.' and string[0:3] in Date._mon):
            return Date._Type.MONTH
        g = re.search('^[1-2][0-9]{3}$',string)   #match a year between 1000 and 2999
        if g:
            return Date._Type.YEAR
        return Date._Type.OTHER
