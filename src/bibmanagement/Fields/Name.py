class Name:
    def __init__(self, str):
        if len(str.strip()) == 0:
            raise ValueError('Name cannot be an empty string')
        self._firstName = None
        self._middleName = None
        self._lastName = None
        self._parse(str)

    @staticmethod
    def _correctCase(str):
        names = str.split()
        if len(names) > 1:
            sep = ' '
            return sep.join([Name._correctCase(s) for s in names])
        else:
            #checking for composed names
            n = names[0].split('-')
            if len(n)>1:
                sep = '-'
                return sep.join([Name._correctCase(s) for s in n])
            else:
                name = n[0]
                return name[0].upper() + name[1:len(name)].lower()

    @staticmethod
    def _abbr(str):
        if len(str.strip()) == 0:
            return ''
        names = str.split()
        if len(names) > 1:
            sep = ' '
            return sep.join([Name._abbr(s) for s in names])
        else:
            #checking for composed names
            n = names[0].split('-')
            if len(n)>1:
                sep = '-'
                return sep.join([Name._abbr(s) for s in n])
            else:
                name = n[0]
                return name[0] + '.'

    def _parse(self, str):
        # Simple parsing, we do not handle 'von' or 'Jr'
        # See https://nwalsh.com/tex/texhelp/bibtx-23.html for how complex it should be
        #
        # If there is a coma, everything before is the family name, first word after is the
        # first name and the rest is the middle names.
        # If no coma, first word is the first name, last one is the family name, the rest is
        # the middle names
        # If multiple comas, everything before the first is the family name, everything
        # between the first and second is the first name, and the rests are middle names
        s = str.split(',')
        if len(s)==1:
            names = s[0].split()
            n = len(names)
            if n==1:
                self._lastName = Name._correctCase(names[0])
            else:
                self._firstName = Name._correctCase(names[0])
                self._lastName = Name._correctCase(names[-1])
                if n>2:
                    sep = ' '
                    self._middleName = Name._correctCase(sep.join(names[1:n-1]))
        else:
            if len(s)==2:
                self._lastName = Name._correctCase(s[0].strip().rstrip())
                names = s[1].split()
                n = len(names)
                self._firstName = Name._correctCase(names[0])
                if n>1:
                    sep = ' '
                    self._middleName = Name._correctCase(sep.join(names[1:n]))
            else:
                self._lastName = Name._correctCase(s[0].strip().rstrip())
                self._firstName = Name._correctCase(s[1].strip().rstrip())
                sep = ' '
                self._middleName = Name._correctCase(sep.join([n.strip().rstrip() for n in s[2:]]))
                if len(s)>3:
                    print("Warning, name with more than 3 components: {0}".format(str))
                #raise ValueError('Name with more than 1 coma (if this is because of a Jr, we do not handle this case for now).')

    @property
    def first(self):
        if self._firstName:
            return self._firstName
        else:
            return ''

    @property
    def middle(self):
        if self._middleName:
            return self._middleName
        else:
            return ''

    @property
    def last(self):
        if self._lastName:
            return self._lastName
        else:
            return ''

    def format(self, formatExpr):
        """ 
        Replace placeholders in formatExpr by the corresponding names.
        Placeholders  can be %First%, %first%, %FIRST%, %F%, %f%, %Middle%, %middle%, %MIDDLE%, %M%, %m%, %Last%, %last%, %LAST%, %L% or %l%.
        %First% will be replaced by the first name in full, with first letter in upper case and other letters in lower case
        %first% will be replaced by the first name, with all letters in lower case
        %FIRST% will be replaced by the first name, with all letters in upper case
        %f% will be replaced by the abbreviation of the first name in lower case
        %F% will be replaced by the abbreviation of the first name in upper case
        The same logic applies for the middle and last names.

        Examples:
        For John Doe, formatExpr="%LAST% (%First%)" returns "DOE (John)", and formatExpr = "%First% %M% %Last%" return "John Doe"
        For Gene Howard Golub, formatExpr="%LAST% (%First%)" returns "GOLUB (Gene)", and formatExpr = "%First% %M% %Last%" return "Gene H. Golub"
        """
        return formatExpr.replace('%First%', self.first) \
                         .replace("%first%", self.first.lower()) \
                         .replace("%FIRST%", self.first.upper()) \
                         .replace('%F%', Name._abbr(self.first))\
                         .replace('%f%', Name._abbr(self.first).lower())\
                         .replace('%Middle%', self.middle) \
                         .replace("%middle%", self.middle.lower()) \
                         .replace("%MIDDLE%", self.middle.lower()) \
                         .replace('%M%', Name._abbr(self.middle))\
                         .replace('%m%', Name._abbr(self.middle).lower())\
                         .replace('%Last%', self.last) \
                         .replace("%last%", self.last.lower()) \
                         .replace("%LAST%", self.last.lower()) \
                         .replace('%L%', Name._abbr(self.last))\
                         .replace('%l%', Name._abbr(self.last).lower())