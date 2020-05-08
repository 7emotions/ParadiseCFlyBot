import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup


def baike( word ) :
    def test_url( soup ) :
        result = soup.find( text=re.compile("百度百科未收录该词条") )
        if result :
            return False
        else:
            return True

    def summary( soup ) :
        word = soup.h1.text 
        if soup.h2 :
            word += soup.h2.text
            print( word )
        if soup.find( class_="lemma-summary" ) :
            sum = soup.find( class_="lemma-summary" ).text
            print(sum)
            return sum

    def start( word ):
        keyword = urllib.parse.urlencode( {"word" : word} )
        response = urllib.request.urlopen( "http://baike.baidu.com/search/word?%s" % keyword )
        html = response.read()
        soup = BeautifulSoup( html , "html.parser" )
        if test_url( soup ) :
            return summary( soup )
        else :
            return ''
    
    try :
        return start( word )
    except AttributeError :
        msg = "百度百科未收录该词条"
        print(msg)
        return msg

if __name__ == '__main__' :
    print(baike('杨万里'))