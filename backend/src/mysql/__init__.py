from html import unescape
import re

def clean_html(input_string):
    # Unescape HTML entities to convert them into regular HTML tags
    unescaped_string = unescape(input_string)

    # Replace the bullet point placeholder with a text bullet point
    unescaped_string = unescaped_string.replace('\n', ' ')
    unescaped_string = unescaped_string.replace('•', '\n•')

    # Strip HTML tags while preserving line breaks
    # clean_text = re.sub(r'\n', ' ', unescaped_string)
    clean_text = re.sub(r'(<[^>]+>|&nbsp;)', ' ', unescaped_string)
    clean_text = re.sub(r'[\r\n]+', '\n', clean_text).strip()
    return clean_text

if __name__ == "__main__":
    # The input HTML-encoded string
    input_string = """&lt;p class=&quot;MsoNormal&quot;&gt;&lt;span style=&quot;font-size:9.0pt;font-family:&amp;quot;Arial&amp;quot;,&amp;quot;sans-serif&amp;quot;;color:black;mso-ansi-language:
    EN-US;mso-bidi-font-weight:bold&quot;&gt;Reliability, portability and accurate counting
    operations&lt;o:p&gt;&lt;/o:p&gt;&lt;/span&gt;&lt;/p&gt;&lt;p class=&quot;MsoNormal&quot;&gt;&lt;span style=&quot;font-size:9.0pt;font-family:&amp;quot;Arial&amp;quot;,&amp;quot;sans-serif&amp;quot;;color:black;mso-ansi-language:
    EN-US;mso-bidi-font-weight:bold&quot;&gt;in one affordable package!&lt;/span&gt;&lt;span style=&quot;font-size:9.0pt;font-family:&amp;quot;Arial&amp;quot;,&amp;quot;sans-serif&amp;quot;;mso-ansi-language:EN-US&quot;&gt;&lt;o:p&gt;&lt;/o:p&gt;&lt;/span&gt;&lt;/p&gt;&lt;p class=&quot;MsoNormal&quot;&gt;&lt;span style=&quot;font-size:9.0pt;font-family:&amp;quot;Arial&amp;quot;,&amp;quot;sans-serif&amp;quot;;color:#E40043;
    mso-ansi-language:EN-US;mso-bidi-font-weight:bold&quot;&gt;•&lt;/span&gt;&lt;span style=&quot;font-size:9.0pt;font-family:&amp;quot;Arial&amp;quot;,&amp;quot;sans-serif&amp;quot;;color:black;mso-ansi-language:
    EN-US;mso-bidi-font-weight:bold&quot;&gt; Dedicated counting keypad providing fast and
    simple operation&lt;o:p&gt;&lt;/o:p&gt;&lt;/span&gt;&lt;/p&gt;&lt;p class=&quot;MsoNormal&quot;&gt;&lt;span style=&quot;font-size:9.0pt;font-family:&amp;quot;Arial&amp;quot;,&amp;quot;sans-serif&amp;quot;;color:#E40043;
    mso-ansi-language:EN-US;mso-bidi-font-weight:bold&quot;&gt;•&lt;/span&gt;&lt;span style=&quot;font-size:9.0pt;font-family:&amp;quot;Arial&amp;quot;,&amp;quot;sans-serif&amp;quot;;color:black;mso-ansi-language:
    EN-US;mso-bidi-font-weight:bold&quot;&gt; Average piece weight (APW) memory speeds up
    counting of commonly counted parts&lt;o:p&gt;&lt;/o:p&gt;&lt;/span&gt;&lt;/p&gt;&lt;p class=&quot;MsoNormal&quot;&gt;





    &lt;/p&gt;&lt;p class=&quot;MsoNormal&quot;&gt;&lt;span style=&quot;font-size:9.0pt;font-family:&amp;quot;Arial&amp;quot;,&amp;quot;sans-serif&amp;quot;;color:#E40043;
    mso-ansi-language:EN-US;mso-bidi-font-weight:bold&quot;&gt;•&lt;/span&gt;&lt;span style=&quot;font-size:9.0pt;font-family:&amp;quot;Arial&amp;quot;,&amp;quot;sans-serif&amp;quot;;color:black;mso-ansi-language:
    EN-US;mso-bidi-font-weight:bold&quot;&gt; Continual recalculation of piece weight and
    high internal resolution 1:300 000 ensures counting accuracy&lt;o:p&gt;&lt;/o:p&gt;&lt;/span&gt;&lt;/p&gt;""" # Shortened for brevity


    print(clean_html(input_string))

