############## CONSTANTS
####### HTML
html_fic_base = """<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}, par {author}</title>

    </head>

    <body style="background-color: #fffffa; padding: 15%; padding-top: 0.5em; line-height: 2em">
    <p style="font-size: 0.9em; text-align: right; margin-bottom: 5em; margin-right: 0.5em">
                Ce texte peut aussi être lu sur
                <a href="SITE_URL/">son site d'origine</a>.
    </p>

        <section style="border: black thin solid; padding: 2em; margin: 1em; margin-bottom: 4em;">
            <header style="text-align: center">
                <h1 style="font-size: 3em; margin-bottom: 0px;line-height: normal;">{title}</h1>
                <p style="font-size: 1.8em; margin-top: 0px">par {author}</p>
            </header>

            <div text-align: justify><i>{summary}</i></div>

        </section>

    {chapters}
    </body>
</html>"""

numbered_chapter_title = """<h2 style="margin-top: 2em">Chapitre {number}</h2>"""


##### PDF #########################################################################################################################
pdf_page_title_style = """
    @page {
        size: A5 portrait;
        margin: 0cm;
        @frame title_frame {        
            left: 0px;
            right: 0px;
            width: 420pt;
            top: 170pt;
            height: 100pt;
        }
        @frame summary_frame {
            left: 50pt;
            width: 320pt;
            top: 310pt;
            height: 200pt;
        }

        @frame credit_frame {
            -pdf-frame-content: credit_content;
            left: 0pt;
            width: 390pt;
            top: 560pt;
            height: 200pt;
        }
    }
"""
pdf_normal_page_style = """
    @page normal_page {
        size: A5 portrait;
        margin: 2cm;

        @frame page_number_frame {
            -pdf-frame-content: page_number_content;
            left: 0pt;
            width: 390pt;
            top: 560pt;
            height: 200pt;
        }
    }
"""

pdf_fic_base = """
<html>

<style>
    {pdf_page_title_style}

    {pdf_normal_page_style}

    body {{
        font-family: serif;
    }}
    h1 {{
        text-align: center;
        font-size: 32pt;
        margin-bottom: 0pt;
    }}
    p {{
        font-size: 12pt;
        text-align: justify;
        word-break: break-word;
        hyphens: auto;
        text-indent: 20pt;
        orphans: 3;
    }}
    .author_name {{
        font-size: 17pt;
        text-align: center;
        line-height: normal;
        margin-top: 0pt;
    }}
    .summary_block {{
        font-size: 12pt;
        font-style: italic;
        line-height: normal;
        text-align: justify;
        word-break: break-word;
        hyphens: auto;
    }}
    .credit_block {{
        font-size: 10pt;
        text-align: right;
    }}
    .page_number {{
        font-size: 9pt;
        text-align: right;
    }}
    .keep_busy {{
        color: white;
    }}

</style>

<body>
    <div id="title_frame">
        <h1>{title}</h1>
        <p class="author_name">{author}</p>
    </div>

    <div id="summary_frame">
        <p class="summary_block">{summary}</p>
    </div>

    <div id="credit_content">
        <p class="credit_block">
            Ce texte peut aussi être lu sur
            <a href="SITE_URL">son site d'origine</a>.
        </p>
    </div>
    
    <pdf:nexttemplate name="normal_page" />        
    <pdf:nextpage>

        {chapters}

    <div id="page_number_content">
        <p class="page_number">
            <span class="keep_busy">.</span><pdf:pagenumber>
        </p>
    </div>


</body>
</html>
"""