import os 
import ast
import  matplotlib.pyplot as plt
from datetime import date
import json
from wordcloud import WordCloud

directory = 'output'

# load employee feedback
with open("data/"+"employee_feedback.json", 'r') as f:
    feedback = json.load(f)["employees"]

# loop through output and process into graphs
for filename in os.listdir(directory):

    emp_summ = ""
    plt.axis('on')
    f = os.path.join(directory, filename)
    scores = []
    dates_s = []
    dates_b = []
    beliefs = []

    if os.path.isfile(f):
        with open(f, 'r') as fil:
            dat = fil.readlines()
        
        # extract id and name
        idx = -1
        id = dat[1].strip()
        name = dat[0]
        del(dat[0])
        del(dat[1])

        # loop through the output and format scores, beliefs, and summary.
        for d in dat:
            idx+=1
            d_s = d.split(':')
            try:
                out = d_s[1].strip()
                try: 
                    out = int(out)
                    scores.append(out)
                    date_new = d_s[0].split('-')
                    new_date = date(int(date_new[0]), int(date_new[1]), int(date_new[2]))
                    dates_s.append(new_date.strftime("%d %b"))
                except:
                    beliefs.append(out)
                    date_new = d_s[0].split('-')
                    new_date = date(int(date_new[0]), int(date_new[1]), int(date_new[2]))
                    dates_b.append(new_date.strftime("%d %b"))
            except:
                if idx == len(dat)-1:
                    emp_summ += d

        # make the plot of mental health scores
        plt.xticks(list(range(0, len(dates_s))), dates_s, rotation='vertical', fontsize='xx-small')
        plt.ylim(0, 10)
        plt.xlabel('Feedback Date')
        plt.ylabel('Mental Health Score')
        plt.title(f'Mental Health Scores: {name}')
        plt.plot(list(range(0, len(scores))), scores, '-o')
        plt.savefig(f"graphs/{id}.png")
        plt.clf()

        # make the word cloud of beliefs
        belief_text = ' '.join(beliefs)
        wc = WordCloud(background_color='white', colormap="Purples", width=800, height=500).generate(belief_text)
        plt.title(f'Special Beliefs - {name}')
        plt.imshow(wc)
        plt.axis('off')
        plt.savefig(f"graphs/{id}wc.png")
        plt.clf()

        # output raw summaries
        with open('summaries/' + id + '_summary.txt', 'w') as summ:
            summ.write(emp_summ + "\n")

            for i in range(0, len(dates_s)):
                summ.write(f'{dates_s[i]};{scores[i]}\n')
            for i in range(0, len(dates_s)):
                summ.write(f'{dates_b[i]};{beliefs[i]}\n')