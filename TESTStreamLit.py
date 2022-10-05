import datetime
from sqlalchemy import null
from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect
import streamlit as st
st.set_page_config(layout="wide")


"""# 2022-23 SoupCord NHL Prediction Contest Entry Form
Welcome to the 2022-23 SoupCord NHL Prediction Contest! Similar to
the classic DownGoesBrown prediction contest in style, this prediction
contest aims to take a different approach, using different questions
to try to keep you in the game for longer... before inevitably 
crushing your hopes at the last minute! This app was originally 
developed for the DGB contest for this year, but DGB wanted to stick 
with comment scraping, so I've repurposed the app with his blessing to
use it for a special contest for the SoupCord!  

Please be sure to include your actual discord handle, including the 
'#', so that I can let you know your final score and placement, just 
in case anything should ever happen to the server or if you decide to 
unsubscribe from Puck Soup (why??) or anything like that. No promises,
but I *might* come up with a silly prize to send to the winner of this
silly contest. 

RULES: For each question, up to 5 answers may be provided to earn
increasing points per correct answer (1 answer = 1 point, 2 answers = 
3 points, 3 answers = 6 points, 4 answers = 10 points, and 5 answers = 
15 points) on a particular question. ANY incorrect answer on a 
particular question will result in 0 points for that question, no 
matter how many right answers were provided. You are _not required_ to 
provide 5 answers for each question, so you can choose whether to take
the risk and go for maximum possible points, or play it safe with a 
few "sure things" to get some points on the board. 

Note that you can "edit" your entry by simply submitting a new entry. Only
your most recent entry will be counted, though all entries will be 
recorded. The contest closes to new entries on 11 Oct 2022 @ 1900 Eastern. 

Good luck! You're gonna need it!
"""



def new_contest_entry():
    with st.form("contest_entry_form"):
        "### Entrant name & discord handle:"
        entrant_name = st.text_input("Your name, server nickname, whatever")
        if len(entrant_name) < 1:
            st.error("Please provide a valid name.")
        entrant_discord = st.text_input("Your proper discord handle (not server nickname)")
        if entrant_discord.find("#") == -1:
            st.error("Please provide a proper discord handle.")

        accepted_teams = ["Anaheim Ducks", "Arizona Coyotes", "Boston Bruins", "Buffalo Sabres", "Calgary Flames", "Carolina Hurricanes", "Chicago Blackhawks", "Colorado Avalanche", "Columbus Blue Jackets", "Dallas Stars", "Detroit Red Wings", "Edmonton Oilers", "Florida Panthers", "Los Angeles Kings", "Minnesota Wild", "Montreal Canadiens", "Nashville Predators", "New Jersey Devils", "New York Islanders", "New York Rangers", "Ottawa Senators", "Philadelphia Flyers", "Pittsburght Penguins", "San Jose Sharks", "Seattle Kraken", "St. Louis Blues", "Tampa Bay Lightning", "Toronto Maple Leafs", "Vancouver Canucks", "Vegas Golden Knights", "Washington Capitals", "Winnipeg Jets"]
        accepted_forwards = ["Adam Henrique", "Jakob Silfverberg", "Ryan Strome", "Frank Vatrano", "Maxime Comtois", "Trevor Zegras", "Mason McTavish", "Nazem Kadri", "Jonathan Huberdeau", "Andrew Mangiapane", "Mikael Backlund", "Milan Lucic", "Blake Coleman", "Elias Lindholm", "Tyler Toffoli", "Dillon Dube", "Connor McDavid", "Leon Draisaitl", "Zach Hyman", "Ryan Nugent-Hopkins", "Evander Kane", "Kailer Yamamoto", "Jesse Puljujarvi", "Warren Foegele", "Anze Kopitar", "Kevin Fiala", "Philip Danault", "Adrian Kempe", "Viktor Arvidsson", "Alex Iafallo", "Quinton Byfield", "Arthur Kaliyev", "Tomas Hertl", "Logan Couture", "Timo Meier", "Kevin Labanc", "Luke Kunin", "Oskar Lindblom", "Alexander Barabanov", "Nick Bonino", "Nico Sturm", "William Eklund", "Jordan Eberle", "Jaden Schwartz", "Andre Burakovsky", "Oliver Bjorkstrand", "Yanni Gourde", "Jared McCann", "Alexander Wennberg", "Joonas Donskoi", "Brandon Tanev", "Shane Wright", "Matthew Beniers", "Elias Pettersson", "Brock Boeser", "Bo Horvat", "JT Miller", "Conor Garland", "Ilya Mikheyev", "Tanner Pearson", "Jason Dickinson", "Andrei Kuzmenko", "Vasiliy Podkolzin", "Nils Hoglander", "Jack Eichel", "Mark Stone", "William Karlsson", "Jonathan Marchessault", "Reilly Smith", "Nicolas Roy", "Chandler Stephenson", "David Pastrnak", "Brad Marchand", "Taylor Hall", "Charlie Coyle", "Jake DeBrusk", "Nick Foligno", "Pavel Zacha", "Craig Smith", "Patrice Bergeron", "Jeff Skinner", "Kyle Okposo", "Alex Tuch", "Victor Olofsson", "Casey Mittelstadt", "Zemgus Girgensons", "Dylan Cozens", "Peyton Krebs", "Dylan Larkin", "Andrew Copp", "Jakub Vrana", "Tyler Bertuzzi", "David Perron", "Robby Fabbri", "Pius Suter", "Oskar Sundquist", "Dominik Kubalik", "Adam Erne", "Lucas Raymond", "Aleksander Barkov", "Matthew Tkachuk", "Sam Reinhart", "Patric Hornqvist", "Sam Bennett", "Carter Verhaeghe", "Anthony Duclair", "Anton Lundell", "Nick Suzuki", "Brendan Gallagher", "Josh Anderson", "Evgeni Dadonov", "Mike Hoffman", "Christian Dvorak", "Joel Armia", "Kirby Dach", "Juraj Slafkovsky", "Cole Caufield", "Sean Monahan", "Jonathan Drouin", "Paul Byron", "Brady Tkachuk", "Joshua Norris", "Claude Giroux", "Alex DeBrincat", "Drake Batherson", "Mathieu Joseph", "Shane Pinto", "Tim Stutzle", "Nikita Kucherov", "Brayden Point", "Steven Stamkos", "Alex Killorn", "Nicholas Paul", "Vladislav Namestnikov", "Anthony Cirelli", "Auston Matthews", "John Tavares", "Mitchell Marner", "William Nylander", "Alexander Kerfoot", "Pierre Engvall", "Calle Jarnkrok", "Sebastian Aho (CAR)", "Andrei Svechnikov", "Jordan Staal", "Teuvo Teravainen", "Jesperi Kotkaniemi", "Martin Necas", "Jesper Fast", "Seth Jarvis", "Max Pacioretty", "Johnny Gaudreau", "Patrik Laine", "Jakub Voracek", "Gustav Nyquist", "Jack Roslovic", "Sean Kuraly", "Yegor Chinakhov", "Kent Johnson", "Cole Sillinger", "Boone Jenner", "Jack Hughes", "Nico Hischier", "Ondrej Palat", "Jesper Bratt", "Tomas Tatar", "Andreas Johnsson", "Miles Wood", "Erik Haula", "Yegor Sharangovich", "Dawson Mercer", "Mathew Barzal", "Anders Lee", "Brock Nelson", "Josh Bailey", "Jean-Gabriel Pageau", "Kyle Palmieri", "Anthony Beauvillier", "Casey Cizikas", "Oliver Wahlstrom", "Artemi Panarin", "Mika Zibanejad", "Chris Kreider", "Vincent Trocheck", "Barclay Goodrow", "Filip Chytil", "Kaapo Kakko", "Alexis Lafreniere", "Kevin Hayes", "James van Reimsdyk", "Cam Atkinson", "Travis Konecny", "Joel Farabee", "Scott Laughton", "Bobby Brink", "Noah Cates", "Sean Coutourier",  "Sidney Crosby", "Evgeni Malkin", "Jake Guentzel", "Jason Zucker", "Bryan Rust", "Rickard Rakell", "Kasperi Kapanen", "Jeff Carter", "Brock McGinn", "Teddy Blueger", "Alex Ovechkin", "Evgeny Kuznetsov", "TJ Oshie", "Anthony Mantha", "Connor Brown", "Lars Eller", "Dylan Strome", "Nicklas Backstrom", "Tom Wilson", "Carl Hagelin", "Clayton Keller", "Nick Schmaltz", "Andrew Ladd", "Lawson Crouse", "Zack Kassian", "Nick Ritchie", "Jack McBain", "Bryan Little", "Patrick Kane", "Jonathan Toews", "Tyler Johnson", "Andreas Athanasiou", "Max Domi", "Lukas Reichel", "Mikko Rantanen", "Gabriel Landeskog", "Nathan MacKinnon", "Valeri Nichushkin", "Artturi Lehkonen", "JT Compher", "Evan Rodrigues", "Alex Newhook", "Tyler Seguin" "Jamie Benn", "Joe Pavelski", "Mason Marchment", "Radek Faksa", "Roope Hintz", "Denis Gurianov", "Jacob Peterson", "Jason Robertson", "Kirill Kaprizov", "Mats Zuccarello", "Joel Eriksson Ek", "Marcus Foligno", "Jordan Greenway", "Tyson Jost", "Matthew Boldy", "Filip Forsberg", "Matt Duchene", "Ryan Johansen", "Mikael Granlund", "Nino Niederreiter", "Colton Sissons", "Philip Tomasino", "Ryan O'Reilly", "Vladimir Tarasenko", "Brayden Schenn", "Pavel Buchnevich", "Brandon Saad", "Jordan Kyrou", "Robert Thomas", "Ivan Barbashev", "Blake Wheeler", "Kyle Connor", "Mark Scheifele", "Nikolaj Ehlers", "Pierre-Luc Dubois", "Adam Lowry", "Mason Appleton", "Morgan Barron", "Cole Perfetti"]
        accepted_defensemen = ["John Klingberg", "Cam Fowler", "Kevin Shattenkirk", "Dmitry Kulikov", "Jamie Drysdale", "Noah Hanifin", "Rasmus Andersson", "Chris Tanev", "Nikita Zadorov", "MacKenzie Weegar", "Oliver Kylington", "Darnell Nurse", "Tyson Barrie", "Cody Ceci", "Brett Kulak", "Evan Bouchard", "Drew Doughty", "Matt Roy", "Sean Walker", "Tobias Bjornfot", "Erik Karlsson", "Marc-Edouard Vlasic", "Mario Ferraro", "Radim Simek", "Jamie Oleksiak", "Vince Dunn", "Adam Larsson", "Justin Schultz", "Carson Soucy", "Quinn Hughes", "Oliver Ekman-Larsson", "Tyler Myers", "Tucker Poolman", "Alex Pietrangelo", "Alec Martinez", "Shea Theodore", "Brayden McNabb", "Zach Whitecloud", "Charlie McAvoy", "Hampus Lindholm", "Brandon Carlo", "Matt Grzelcyk", "Derek Forbort", "Mike Reilly", "Rasmus Dahlin", "Ilya Lyubushkin", "Henri Jokiharju", "Mattias Samuelsson", "Owen Power", "Ben Chiarot", "Filip Hronek", "Olli Maatta", "Moritz Seider", "Aaron Ekblad", "Brandon Montour", "Gustav Forsling", "Radko Gudas", "Michael Matheson", "Joel Edmundson", "David Savard", "Justin Barron", "Thomas Chabot", "Nikita Zaitsev", "Travis Hamonic", "Artem Zub", "Jake Sanderson", "Victor Hedman", "Mikhail Sergachev", "Ian Cole", "Erik Cernak", "Philippe Myers", "Morgan Reilly", "Jake Muzzin", "TJ Brodie", "Justin Holl", "Jaccob Slavin", "Brent Burns", "Brady Skjei", "Brett Pesce", "Ethan Bear", "Jake Gardiner", "Zachary Werenski", "Erik Gudbranson", "Vladislav Gavrikov", "Adam Boqvist", "Jake Bean", "Dougie Hamilton", "John Marino", "Damon Severson", "Ryan Graves", "Simon Nemec", "Ryan Pulock", "Adam Pelech", "Noah Dobson", "Alexander Romanov", "Adam Fox", "Jacob Trouba", "Ryan Lindgren", "Zachary Jones", "K'Andre Miller", "Braden Schneider", "Ivan Provorov", "Rasmus Ristolainen", "Anthony DeAngelo", "Travis Sanheim", "Cam York", "Ronnie Attard", "Ryan Ellis", "Jeff Petry", "Kris Letang", "Brian Dumoulin", "Marcus Pettersson", "Jan Rutta", "Ty Smith", "John Carlson", "Dmitry Orlov", "Nick Jensen", "Martin Fehervary", "Jakob Chychrun", "Shayne Gostisbehere", "Patrik Nemeth", "Janis Moser", "Seth Jones", "Connor Murphy", "Alex Vlasic", "Jake McCabe", "Cale Makar", "Erik Johnson", "Samuel Girard", "Josh Manson", "Devon Toews", "Bowen Byram", "Miro Heiskanen", "Esa Lindell", "Ryan Suter", "Thomas Harley", "Jared Spurgeon", "Jonas Brodin", "Matt Dumba", "Jacob Middleton", "Alex Goligoski", "Roman Josi", "Ryan McDonagh", "Mattias Ekholm", "Dante Fabbro", "Jeremy Lauzon", "Justin Faulk", "Torey Krug", "Colton Parayko", "Nick Leddy", "Marco Scandella", "Joshua Morrissey", "Nate Schmidt", "Neal Pionk", "Brenden Dillon", "Dylan DeMelo", "Dylan Samberg", "Ville Heinola"]
        accepted_goalies = ["John Gibson", "Anthony Stolarz", "Jacob Markstrom", "Dan Vladar", "Jack Campbell", "Stuart Skinner", "Jonathan Quick", "Cal Petersen", "Kaapo Kahkonen", "James Reimer", "Philip Grubauer", "Chris Driedger", "Martin Jones", "Thatcher Demko", "Spencer Martin", "Laurent Brossoit", "Adin Hill", "Logan Thompson", "Linus Ullmark", "Jeremy Swayman", "Eric Comrie", "Craig Anderson", "Ville Husso", "Alex Nedeljkovic", "Sergei Bobrovsky", "Spencer Knight", "Jake Allen", "Samuel Montembeault", "Cam Talbot", "Anton Forsberg", "Andrei Vasilevskiy", "Brian Elliott", "Matt Murray", "Ilya Samsonov", "Frederick Andersen", "Antti Raanta", "Elvis Merzlikins", "Joonas Korpisalo", "Vitek Vanecek", "MacKenzie Blackwood", "Semyon Varlamov", "Ilya Sorokin", "Igor Shesterkin", "Jaroslav Halak", "Carter Hart", "Felix Sandstrom", "Tristan Jarry", "Casey DeSmith", "Darcy Kuemper", "Charlie Lindgren", "Karel Vejmelka", "Petr Mrazek", "Alex Stalock", "Alexandar Georgiev", "Pavel Francouz", "Jake Oettinger", "Scott Wedgewood", "Marc-Andre Fleury", "Filip Gustavsson", "Juuse Saros", "Kevin Lankinen", "Jordan Binnington", "Thomas Greiss", "Connor Hellebuyck", "David Rittich"]
        accepted_skaters = accepted_forwards.copy()
        for defenseman in accepted_defensemen:
            accepted_skaters.append(defenseman)
        "### Q1: Select up to five teams which will have a PP% and PK% totalling *over* 100.00% this season:"
        "Note: 16 teams did this last year."
        col1, col2, col3, col4, col5 = st.columns(5)
        q1a1 = col1.selectbox("Question 1, Answer 1", ["PASS"] + accepted_teams)
        q1a2 = col2.selectbox("Question 1, Answer 2", ["PASS"] + accepted_teams)
        q1a3 = col3.selectbox("Question 1, Answer 3", ["PASS"] + accepted_teams)
        q1a4 = col4.selectbox("Question 1, Answer 4", ["PASS"] + accepted_teams)
        q1a5 = col5.selectbox("Question 1, Answer 5", ["PASS"] + accepted_teams)
        temp_answers = [q1a1, q1a2, q1a3, q1a4, q1a5]
        for answer in temp_answers:
            if answer == "PASS":
                continue
            else:
                if temp_answers.count(answer) != 1:
                    answer_index = temp_answers.index(answer)
                    temp_answers.pop(answer_index)
                    temp_answers.insert(answer_index, "PASS")
                    st.write("Removed duplicate answer!")
        q1a1, q1a2, q1a3, q1a4, q1a5 = temp_answers
        "### Q2: Select up to five teams which will have a PP% and PK% totalling *under* 100.00% this season:"
        "Note: 16 teams did this last year."
        col1, col2, col3, col4, col5 = st.columns(5)
        q2a1 = col1.selectbox("Question 2, Answer 1", ["PASS"] + accepted_teams)
        q2a2 = col2.selectbox("Question 2, Answer 2", ["PASS"] + accepted_teams)
        q2a3 = col3.selectbox("Question 2, Answer 3", ["PASS"] + accepted_teams)
        q2a4 = col4.selectbox("Question 2, Answer 4", ["PASS"] + accepted_teams)
        q2a5 = col5.selectbox("Question 2, Answer 5", ["PASS"] + accepted_teams)
        temp_answers = [q2a1, q2a2, q2a3, q2a4, q2a5]
        for answer in temp_answers:
            if answer == "PASS":
                continue
            else:
                if temp_answers.count(answer) != 1:
                    answer_index = temp_answers.index(answer)
                    temp_answers.pop(answer_index)
                    temp_answers.insert(answer_index, "PASS")
                    st.write("Removed duplicate answer!")
            q2a1, q2a2, q2a3, q2a4, q2a5 = temp_answers
        "### Q3: Select up to 5 goalies to earn more than 25 wins this season:"
        "Note: 18 goalies did this last year"
        col1, col2, col3, col4, col5 = st.columns(5)
        q3a1 = col1.selectbox("Question 3, Answer 1", ["PASS"] + accepted_goalies)
        q3a2 = col2.selectbox("Question 3, Answer 2", ["PASS"] + accepted_goalies)
        q3a3 = col3.selectbox("Question 3, Answer 3", ["PASS"] + accepted_goalies)
        q3a4 = col4.selectbox("Question 3, Answer 4", ["PASS"] + accepted_goalies)
        q3a5 = col5.selectbox("Question 3, Answer 5", ["PASS"] + accepted_goalies)
        temp_answers = [q3a1, q3a2, q3a3, q3a4, q3a5]
        for answer in temp_answers:
            if answer == "PASS":
                continue
            else:
                if temp_answers.count(answer) != 1:
                    answer_index = temp_answers.index(answer)
                    temp_answers.pop(answer_index)
                    temp_answers.insert(answer_index, "PASS")
                    st.write("Removed duplicate answer!")
            q3a1, q3a2, q3a3, q3a4, q3a5 = temp_answers
        "### Q4: Select up to 5 goalies to earn at least 3 shutouts this year:"
        "Note: 19 goalies did this last year"
        col1, col2, col3, col4, col5 = st.columns(5)
        q4a1 = col1.selectbox("Question 4, Answer 1", ["PASS"] + accepted_goalies)
        q4a2 = col2.selectbox("Question 4, Answer 2", ["PASS"] + accepted_goalies)
        q4a3 = col3.selectbox("Question 4, Answer 3", ["PASS"] + accepted_goalies)
        q4a4 = col4.selectbox("Question 4, Answer 4", ["PASS"] + accepted_goalies)
        q4a5 = col5.selectbox("Question 4, Answer 5", ["PASS"] + accepted_goalies)
        temp_answers = [q4a1, q4a2, q4a3, q4a4, q4a5]
        for answer in temp_answers:
            if answer == "PASS":
                continue
            else:
                if temp_answers.count(answer) != 1:
                    answer_index = temp_answers.index(answer)
                    temp_answers.pop(answer_index)
                    temp_answers.insert(answer_index, "PASS")
                    st.write("Removed duplicate answer!")
            q4a1, q4a2, q4a3, q4a4, q4a5 = temp_answers
        "### Q5: Select up to 5 goalies to earn at least 2 points this year:"
        "Note: 10 goalies did this last year"
        col1, col2, col3, col4, col5 = st.columns(5)
        q5a1 = col1.selectbox("Question 5, Answer 1", ["PASS"] + accepted_goalies)
        q5a2 = col2.selectbox("Question 5, Answer 2", ["PASS"] + accepted_goalies)
        q5a3 = col3.selectbox("Question 5, Answer 3", ["PASS"] + accepted_goalies)
        q5a4 = col4.selectbox("Question 5, Answer 4", ["PASS"] + accepted_goalies)
        q5a5 = col5.selectbox("Question 5, Answer 5", ["PASS"] + accepted_goalies)
        temp_answers = [q5a1, q5a2, q5a3, q5a4, q5a5]
        for answer in temp_answers:
            if answer == "PASS":
                continue
            else:
                if temp_answers.count(answer) != 1:
                    answer_index = temp_answers.index(answer)
                    temp_answers.pop(answer_index)
                    temp_answers.insert(answer_index, "PASS")
                    st.write("Removed duplicate answer!")
            q5a1, q5a2, q5a3, q5a4, q5a5 = temp_answers
        "### Q6: Select up to 5 defensemen to earn at least 2 *shorthanded* points this year:"
        "Note: 26 defensemen did this last year"
        col1, col2, col3, col4, col5 = st.columns(5)
        q6a1 = col1.selectbox("Question 6, Answer 1", ["PASS"] + accepted_defensemen)
        q6a2 = col2.selectbox("Question 6, Answer 2", ["PASS"] + accepted_defensemen)
        q6a3 = col3.selectbox("Question 6, Answer 3", ["PASS"] + accepted_defensemen)
        q6a4 = col4.selectbox("Question 6, Answer 4", ["PASS"] + accepted_defensemen)
        q6a5 = col5.selectbox("Question 6, Answer 5", ["PASS"] + accepted_defensemen)
        temp_answers = [q6a1, q6a2, q6a3, q6a4, q6a5]
        for answer in temp_answers:
            if answer == "PASS":
                continue
            else:
                if temp_answers.count(answer) != 1:
                    answer_index = temp_answers.index(answer)
                    temp_answers.pop(answer_index)
                    temp_answers.insert(answer_index, "PASS")
                    st.write("Removed duplicate answer!")
            q6a1, q6a2, q6a3, q6a4, q6a5 = temp_answers
        "### Q7: Select up to 5 defensemen to earn at least 20 *powerplay* points this year:"
        "Note:15 defensemen did this last year"
        col1, col2, col3, col4, col5 = st.columns(5)
        q7a1 = col1.selectbox("Question 7, Answer 1", ["PASS"] + accepted_defensemen)
        q7a2 = col2.selectbox("Question 7, Answer 2", ["PASS"] + accepted_defensemen)
        q7a3 = col3.selectbox("Question 7, Answer 3", ["PASS"] + accepted_defensemen)
        q7a4 = col4.selectbox("Question 7, Answer 4", ["PASS"] + accepted_defensemen)
        q7a5 = col5.selectbox("Question 7, Answer 5", ["PASS"] + accepted_defensemen)
        temp_answers = [q7a1, q7a2, q7a3, q7a4, q7a5]
        for answer in temp_answers:
            if answer == "PASS":
                continue
            else:
                if temp_answers.count(answer) != 1:
                    answer_index = temp_answers.index(answer)
                    temp_answers.pop(answer_index)
                    temp_answers.insert(answer_index, "PASS")
                    st.write("Removed duplicate answer!")
            q7a1, q7a2, q7a3, q7a4, q7a5 = temp_answers
        "### Q8: Select up to 5 forwards to earn a hat trick this year:"
        "Note: 102 hat tricks were scored last year, by 84 players."
        col1, col2, col3, col4, col5 = st.columns(5)
        q8a1 = col1.selectbox("Question 8, Answer 1", ["PASS"] + accepted_forwards)
        q8a2 = col2.selectbox("Question 8, Answer 2", ["PASS"] + accepted_forwards)
        q8a3 = col3.selectbox("Question 8, Answer 3", ["PASS"] + accepted_forwards)
        q8a4 = col4.selectbox("Question 8, Answer 4", ["PASS"] + accepted_forwards)
        q8a5 = col5.selectbox("Question 8, Answer 5", ["PASS"] + accepted_forwards)
        temp_answers = [q8a1, q8a2, q8a3, q8a4, q8a5]
        for answer in temp_answers:
            if answer == "PASS":
                continue
            else:
                if temp_answers.count(answer) != 1:
                    answer_index = temp_answers.index(answer)
                    temp_answers.pop(answer_index)
                    temp_answers.insert(answer_index, "PASS")
                    st.write("Removed duplicate answer!")
            q8a1, q8a2, q8a3, q8a4, q8a5 = temp_answers
        "### Q9: Select up to 5 forwards to earn at least 1.00 PIM/game (minimum 40 GP) this year:"
        "Note: 36 forwards did this last year"
        "Note #2: This list does not include players making under $2M who are not on ELC's, which reduces the field a bit"
        col1, col2, col3, col4, col5 = st.columns(5)
        q9a1 = col1.selectbox("Question 9, Answer 1", ["PASS"] + accepted_forwards)
        q9a2 = col2.selectbox("Question 9, Answer 2", ["PASS"] + accepted_forwards)
        q9a3 = col3.selectbox("Question 9, Answer 3", ["PASS"] + accepted_forwards)
        q9a4 = col4.selectbox("Question 9, Answer 4", ["PASS"] + accepted_forwards)
        q9a5 = col5.selectbox("Question 9, Answer 5", ["PASS"] + accepted_forwards)
        temp_answers = [q9a1, q9a2, q9a3, q9a4, q9a5]
        for answer in temp_answers:
            if answer == "PASS":
                continue
            else:
                if temp_answers.count(answer) != 1:
                    answer_index = temp_answers.index(answer)
                    temp_answers.pop(answer_index)
                    temp_answers.insert(answer_index, "PASS")
                    st.write("Removed duplicate answer!")
            q9a1, q9a2, q9a3, q9a4, q9a5 = temp_answers
        "### Q10: Select up to 5 skaters to earn at least 1.00 points/game (minimum 50 GP) this year:"
        "Note: 45 skaters did this last year"
        col1, col2, col3, col4, col5 = st.columns(5)
        q10a1 = col1.selectbox("Question 10, Answer 1", ["PASS"] + accepted_skaters)
        q10a2 = col2.selectbox("Question 10, Answer 2", ["PASS"] + accepted_skaters)
        q10a3 = col3.selectbox("Question 10, Answer 3", ["PASS"] + accepted_skaters)
        q10a4 = col4.selectbox("Question 10, Answer 4", ["PASS"] + accepted_skaters)
        q10a5 = col5.selectbox("Question 10, Answer 5", ["PASS"] + accepted_skaters)
        temp_answers = [q10a1, q10a2, q10a3, q10a4, q10a5]
        for answer in temp_answers:
            if answer == "PASS":
                continue
            else:
                if temp_answers.count(answer) != 1:
                    answer_index = temp_answers.index(answer)
                    temp_answers.pop(answer_index)
                    temp_answers.insert(answer_index, "PASS")
                    st.write("Removed duplicate answer!")
            q10a1, q10a2, q10a3, q10a4, q10a5 = temp_answers
        submitted = st.form_submit_button("Submit your entry!")
        if submitted:
            # Create timestamp of submission
            submission_time = datetime.datetime.now()
            # Use Shillelagh to insert the info to the spreadsheet
            credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], 
                scopes=["https://www.googleapis.com/auth/spreadsheets",],)
            connection = connect(":memory:", adapter_kwargs={
                "gsheetsapi" : { 
                "service_account_info" : {
                    "type" : st.secrets["gcp_service_account"]["type"],
                    "project_id" : st.secrets["gcp_service_account"]["project_id"],
                    "private_key_id" : st.secrets["gcp_service_account"]["private_key_id"],
                    "private_key" : st.secrets["gcp_service_account"]["private_key"],
                    "client_email" : st.secrets["gcp_service_account"]["client_email"],
                    "client_id" : st.secrets["gcp_service_account"]["client_id"],
                    "auth_uri" : st.secrets["gcp_service_account"]["auth_uri"],
                    "token_uri" : st.secrets["gcp_service_account"]["token_uri"],
                    "auth_provider_x509_cert_url" : st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
                    "client_x509_cert_url" : st.secrets["gcp_service_account"]["client_x509_cert_url"],
                    }
                },
            })
            cursor = connection.cursor()
            sheet_url = st.secrets["private_gsheets_url"]

            # Troubleshooting for "Couldn't extract column labels from sheet"
            test_query = f'SELECT * FROM "{sheet_url}"'
            for row in cursor.execute(test_query):
                print(row)

            query = f'INSERT INTO "{sheet_url}" VALUES ("{entrant_name}", "{entrant_discord}", "{submission_time}", "{q1a1}", "{q1a2}", "{q1a3}", "{q1a4}", "{q1a5}", "{q2a1}", "{q2a2}", "{q2a3}", "{q2a4}", "{q2a5}", "{q3a1}", "{q3a2}", "{q3a3}", "{q3a4}", "{q3a5}", "{q4a1}", "{q4a2}", "{q4a3}", "{q4a4}", "{q4a5}", "{q5a1}", "{q5a2}", "{q5a3}", "{q5a4}", "{q5a5}", "{q6a1}", "{q6a2}", "{q6a3}", "{q6a4}", "{q6a5}", "{q7a1}", "{q7a2}", "{q7a3}", "{q7a4}", "{q7a5}", "{q8a1}", "{q8a2}", "{q8a3}", "{q8a4}", "{q8a5}", "{q9a1}", "{q9a2}", "{q9a3}", "{q9a4}", "{q9a5}", "{q10a1}", "{q10a2}", "{q10a3}", "{q10a4}", "{q10a5}")'
            cursor.execute(query)
            st.write(f"{entrant_name}, your entry associated with {entrant_discord} has been submitted as of {submission_time} with the following selections:  \nQuestion 1:{q1a1}, {q1a2}, {q1a3}, {q1a4}, {q1a5}  \nQuestion 2:{q2a1}, {q2a2}, {q2a3}, {q2a4}, {q2a5}  \nQuestion 3:{q3a1}, {q3a2}, {q3a3}, {q3a4}, {q3a5}  \nQuestion 4:{q4a1}, {q4a2}, {q4a3}, {q4a4}, {q4a5}  \nQuestion 5:{q5a1}, {q5a2}, {q5a3}, {q5a4}, {q5a5}  \nQuestion 6:{q6a1}, {q6a2}, {q6a3}, {q6a4}, {q6a5}  \nQuestion 7:{q7a1}, {q7a2}, {q7a3}, {q7a4}, {q7a5}  \nQuestion 8:{q8a1}, {q8a2}, {q8a3}, {q8a4}, {q8a5}  \nQuestion 9:{q9a1}, {q9a2}, {q9a3}, {q9a4}, {q9a5}  \nQuestion 10:{q10a1}, {q10a2}, {q10a3}, {q10a4}, {q10a5}")
        

def retrieve_last_entry():
    with st.form("retrieve_entry_form"):
        entrant_discord = st.text_input("Your proper discord handle (not server nickname)")
        if entrant_discord.find("#") == -1:
            st.error("Please provide a proper discord handle.")
        submitted = st.form_submit_button("Find my last entry!")
        if submitted:
            # Use Shillelagh to retrieve the info from the spreadsheet
            credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], 
                scopes=["https://www.googleapis.com/auth/spreadsheets",],)
            connection = connect(":memory:", adapter_kwargs={
                "gsheetsapi" : { 
                "service_account_info" : {
                    "type" : st.secrets["gcp_service_account"]["type"],
                    "project_id" : st.secrets["gcp_service_account"]["project_id"],
                    "private_key_id" : st.secrets["gcp_service_account"]["private_key_id"],
                    "private_key" : st.secrets["gcp_service_account"]["private_key"],
                    "client_email" : st.secrets["gcp_service_account"]["client_email"],
                    "client_id" : st.secrets["gcp_service_account"]["client_id"],
                    "auth_uri" : st.secrets["gcp_service_account"]["auth_uri"],
                    "token_uri" : st.secrets["gcp_service_account"]["token_uri"],
                    "auth_provider_x509_cert_url" : st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
                    "client_x509_cert_url" : st.secrets["gcp_service_account"]["client_x509_cert_url"],
                    }
                },
            })
            cursor = connection.cursor()
            sheet_url = st.secrets["private_gsheets_url"]

            # Intended behavior
            # query = f'SELECT * FROM "{sheet_url}" WHERE B = {entrant_discord}'
            # st.write(f"These are the entries that have been submitted for the contest using the handle {entrant_discord}:")
            # for row in cursor.execute(query):
            #    print(row)

            # troubleshooting
            query = f'SELECT * FROM "{sheet_url}"'
            st.write(f"These are the entries that have been submitted for the contest using the handle {entrant_discord}:")
            response = cursor.execute(query)
            response = response.fetchall()
            st.write(response)

            

sidebar_options = ["New contest entry", "Check last entry"]
user_decision = st.sidebar.selectbox("Enter a new contest entry, or check your last entry?", sidebar_options)
if user_decision == sidebar_options[0]:
    new_contest_entry()
else:
    retrieve_last_entry()
