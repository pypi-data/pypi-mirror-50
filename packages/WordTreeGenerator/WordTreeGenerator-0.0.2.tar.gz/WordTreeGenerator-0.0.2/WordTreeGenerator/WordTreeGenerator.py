import pandas as pd
import logging
from IPython.core.display import display, HTML
from IPython.display import IFrame


class WordTreeGenerator:
    def __init__(self, word, file_name, file_output_name, content_column = 'Content'):
        self.word = word
        self.file_name = file_name
        self.file_output_name = file_output_name
        self.content_column = content_column
        self.part1 = """<html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
          google.charts.load('current', {packages:['wordtree']});
          google.charts.setOnLoadCallback(drawChart);

          function drawChart() {
            var data = google.visualization.arrayToDataTable("""

        self.part2 = """
                )
                var options = {

                  wordtree: {
                    format: 'implicit',
                    word:'"""

        self.part3 = """',
                        type:'double'
                      }
                    };

                    var chart = new google.visualization.WordTree(document.getElementById('wordtree_basic'));
                    chart.draw(data, options);
                  }
                </script>
              </head>
              <body>
                <div id="wordtree_basic" style="width: 900px; height: 500px;"></div>
              </body>
            </html>"""
        logging.debug('Class WordTreeGenerator initialized')
        
    def generate_word_tree(self):
        self.read_data()
        logging.debug('Data Read to Build Word Tree')
        self.filter_data()
        logging.debug('Data Filtered')
        self.generate_html()
        logging.debug('HTML Generated')
        self.save_html()
        logging.debug('HTML Saved')
        
    def word_in_msg(self, msg):
        if type(msg) is str:
            return self.word in msg
        else:
            return False
        
    def read_data(self):
        if type(self.file_name) == str:
            self.data = pd.read_csv(self.file_name,sep='|',encoding='utf-8')
        else:
            self.data = self.file_name
            
    def get_data(self):
        return self.data
    
    def filter_data(self):
        self.messages = self.data[self.data[self.content_column].apply(self.word_in_msg)][self.content_column].values
    
    def generate_html(self):
        msgs_list = []
        for i in range(len(self.messages)):  
            msg = []
            msg.append(self.messages[i])
            msgs_list.append(msg)

        self.html_code = self.part1 + str(msgs_list[0:]) + self.part2 + self.word + self.part3
    
    def get_html(self):
        return self.html_code

    def save_html(self):
        arq_html = open(self.file_output_name + '.html', 'w', encoding='utf-8')
        arq_html.write(self.html_code)
        arq_html.close()

    def show_html(self, wt_width=700, wt_height=600):    
        IFrame(src=self.file_output_name + '.html', width=wt_width, height=wt_height)
