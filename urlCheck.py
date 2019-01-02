# -*- coding: utf-8 -*-

trueURLExample = [
"http://foo.com/blah_blah",
"http://foo.com/blah_blah/",
"http://foo.com/blah_blah_(wikipedia)",
"http://foo.com/blah_blah_(wikipedia)_(again)",
"http://www.example.com/wpstyle/?p=364",
"https://www.example.com/foo/?bar=baz&inga=42&quux",
"http://userid:password@example.com:8080",
"http://userid:password@example.com:8080/",
"http://userid@example.com",
"http://userid@example.com/",
"http://userid@example.com:8080",
"http://userid@example.com:8080/",
"http://userid:password@example.com",
"http://userid:password@example.com/",
"http://142.42.1.1/",
"http://142.42.1.1:8080/",
"http://foo.com/blah_(wikipedia)#cite-1",
"http://foo.com/blah_(wikipedia)_blah#cite-1",
"http://foo.com/(something)?after=parens",
"http://code.google.com/events/#&product=browser",
"http://j.mp",
"ftp://foo.bar/baz",
"http://foo.bar/?q=Test%20URL-encoded%20stuff",
"http://-.~_!$&'()*+,;=:%40:80%2f::::::@example.com",
"http://1337.net",
"http://a.b-c.de",
"http://223.255.255.254"]

falseURLExample = [
"http://",
"http://.",
"http://..",
"http://../",
"http://?",
"http://??",
"http://??/",
"http://#",
"http://##",
"http://##/",
"http://foo.bar?q=Spaces should be encoded"
"//",
"//a",
"///a",
"///",
"http:///a",
"foo.com,",
"rdar://1234",
"h://test",
"http:// shouldfail.com",
":// should fail",
"http://foo.bar/foo(bar)baz quux",
"ftps://foo.bar/",
"http://-error-.invalid/",
"http://a.b--c.de/",
"http://-a.b.co",
"http://a.b-.co",
"http://0.0.0.0",
"http://10.1.1.0",
"http://10.1.1.255",
"http://224.1.1.1",
"http://1.1.1.1.1",
"http://123.123.123",
"http://3628126748",
"http://.www.foo.bar/",
"http://www.foo.bar./",
"http://.www.foo.bar./",
"http://10.1.1.1"]

import re
def isValidURL(url):
    URL_REGEX = re.compile(
        u"^"
        # protocol identifier
        u"(?:(?:https?|ftp)://)"
        # user:pass authentication
        u"(?:\S+(?::\S*)?@)?"
        u"(?:"
        # IP address exclusion
        # private & local networks
        u"(?!(?:10|127)(?:\.\d{1,3}){3})"
        u"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
        u"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
        # IP address dotted notation octets
        # excludes loopback network 0.0.0.0
        # excludes reserved space >= 224.0.0.0
        # excludes network & broadcast addresses
        # (first & last IP address of each class)
        u"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
        u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
        u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
        u"|"
        # host name
        u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
        # domain name
        u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
        # TLD identifier
        u"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
        u")"
        # port number
        u"(?::\d{2,5})?"
        # resource path
        u"(?:/\S*)?"
        u"$"
        , re.UNICODE)
    if URL_REGEX.match(url) == None:
        return False
    else:
        return True

print ("Should all be True")
for url in trueURLExample:
    print (isValidURL(url))

print ("Should all be False")
for url in falseURLExample:
    print (isValidURL(url))