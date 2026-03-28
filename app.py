from flask import Flask, render_template, request, jsonify
from ytmusicapi import YTMusic
import random
import os
# This finds the exact folder where app.py is located
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

yt = YTMusic() # No auth needed for public search


GENRE_SEEDS = {
    "Rock": [
        "Led Zeppelin", "Nirvana", "Pink Floyd", "Queen", "The Rolling Stones", "AC/DC", "Fleetwood Mac", "The Beatles",
        "Radiohead", "The Who", "Guns N' Roses", "The Doors", "Red Hot Chili Peppers", "U2", "Pearl Jam", "The Clash", 
        "The Ramones", "The Strokes", "Arctic Monkeys", "The Killers", "Muse", "Foo Fighters", "Green Day", 
        "The Smashing Pumpkins", "The White Stripes", "The Black Keys", "The Velvet Underground", "The Cure", "The Pixies", 
        "The National", "Tame Impala", "Kings of Leon", "Deep Purple", "Black Sabbath", "The Kinks", "Cream", "Lynyrd Skynyrd", 
        "Journey", "Def Leppard", "Bon Jovi", "Oasis", "Blur", "Linkin Park", "Imagine Dragons", "Coldplay", "The Police", 
        "Dire Straits", "The Beach Boys", "Tom Petty", "Bruce Springsteen"
    ],
    "Blues": [
        "B.B. King", "Muddy Waters", "Stevie Ray Vaughan", "Buddy Guy", "Robert Johnson", "Howlin' Wolf", "John Lee Hooker", 
        "Etta James", "Albert King", "T-Bone Walker", "Koko Taylor", "Elmore James", "Freddie King", "Son House", 
        "Blind Lemon Jefferson", "Big Mama Thornton", "Bonnie Raitt", "Gary Clark Jr.", "Joe Bonamassa", "Shemekia Copeland",
        "Lead Belly", "Lightnin' Hopkins", "Mississippi John Hurt", "Otis Rush", "Junior Wells", "Taj Mahal", "Ry Cooder", 
        "Keb' Mo'", "Christone Kingfish Ingram", "Rory Gallagher", "Beth Hart", "Samantha Fish", "Kenny Wayne Shepherd", 
        "Jimmie Vaughan", "Luther Allison", "Magic Sam", "Willie Dixon", "Big Bill Broonzy", "Pinetop Perkins", "Sonny Boy Williamson",
        "Little Walter", "James Cotton", "Bobby Blue Bland", "Big Joe Turner", "Ruth Brown", "Sister Rosetta Tharpe", 
        "Clarence Gatemouth Brown", "Albert Collins", "Johnny Winter", "Roy Buchanan"
    ],
    "Metal": [
        "Metallica", "Iron Maiden", "Black Sabbath", "Pantera", "Slayer", "Megadeth", "Judas Priest", "Tool", "System of a Down", 
        "Lamb of God", "Avenged Sevenfold", "Slipknot", "Anthrax", "Sepultura", "Dio", "Motörhead", "Rammstein", "Disturbed", 
        "Korn", "Trivium", "Ghost", "Dream Theater", "Opeth", "Mastodon", "Gojira", "Nightwish", "In Flames", "Children of Bodom", 
        "Sabatone", "Killswitch Engage", "Bullet for My Valentine", "Five Finger Death Punch", "Amon Amarth", "Behemoth", 
        "Cannibal Corpse", "Death", "Napalm Death", "Meshuggah", "Between the Buried and Me", "Porcupine Tree", "Helloween", 
        "Blind Guardian", "Stratovarius", "Manowar", "Venom", "Mercyful Fate", "King Diamond", "Celtic Frost", "Bathory", "Hellhammer"
    ],
    "Pop": [
        "Michael Jackson", "Madonna", "Prince", "Taylor Swift", "Beyonce", "The Beatles", "Britney Spears", "Justin Timberlake", 
        "Katy Perry", "Lady Gaga", "Ariana Grande", "Rihanna", "Ed Sheeran", "Bruno Mars", "Shakira", "Dua Lipa", "The Weeknd", 
        "Maroon 5", "Justin Bieber", "Sia", "Adele", "Whitney Houston", "Mariah Carey", "Janet Jackson", "George Michael", 
        "Elton John", "ABBA", "Bee Gees", "Cher", "Celine Dion", "Billie Eilish", "Olivia Rodrigo", "Harry Styles", "Shawn Mendes", 
        "Camila Cabello", "Selena Gomez", "Demi Lovato", "Miley Cyrus", "Halsey", "Lorde", "Lana Del Rey", "Doja Cat", 
        "Post Malone", "Sam Smith", "Kelly Clarkson", "P!nk", "Christina Aguilera", "Gwen Stefani", "Fergie", "Nelly Furtado"
    ],
    "Hip-Hop": [
        "Tupac Shakur", "The Notorious B.I.G.", "Jay-Z", "Eminem", "Kanye West", "Drake", "Nas", "Kendrick Lamar", "Lil Wayne", 
        "Snoop Dogg", "Ice Cube", "Missy Elliott", "OutKast", "Cardi B", "Migos", "Travis Scott", "J. Cole", "Nicki Minaj", 
        "Future", "Post Malone", "21 Savage", "Dr. Dre", "50 Cent", "LL Cool J", "Run-D.M.C.", "Public Enemy", "Wu-Tang Clan", 
        "A Tribe Called Quest", "Rakim", "Big Daddy Kane", "Lauryn Hill", "Busta Rhymes", "DMX", "Method Man", "Redman", 
        "Ghostface Killah", "Raekwon", "Andre 3000", "E-40", "Mac Miller", "Logic", "Tyler, The Creator", "ASAP Rocky", 
        "Schoolboy Q", "Vince Staples", "Joey Badass", "Chance the Rapper", "Big Sean", "Young Thug", "Gunna"
    ],
    "Jazz": [
        "Miles Davis", "John Coltrane", "Louis Armstrong", "Duke Ellington", "Charlie Parker", "Thelonious Monk", "Billie Holiday", 
        "Ella Fitzgerald", "Chet Baker", "Herbie Hancock", "Sonny Rollins", "Dizzy Gillespie", "Count Basie", "Sarah Vaughan", 
        "Art Blakey", "Stan Getz", "Wynton Marsalis", "Charles Mingus", "Nina Simone", "Dave Brubeck", "Wes Montgomery", 
        "Django Reinhardt", "Stéphane Grappelli", "Oscar Peterson", "McCoy Tyner", "Chick Corea", "Keith Jarrett", "Wayne Shorter", 
        "Joe Henderson", "Dexter Gordon", "Cannonball Adderley", "Freddie Hubbard", "Lee Morgan", "Clifford Brown", "Max Roach", 
        "Tony Williams", "Elvin Jones", "Pharoah Sanders", "Alice Coltrane", "Sun Ra", "Ornette Coleman", "Cecil Taylor", 
        "Kamasi Washington", "Robert Glasper", "Esperanza Spalding", "Gregory Porter", "Diana Krall", "Norah Jones", 
        "Jamie Cullum", "Michael Bublé"
    ]
}


def get_50_hybrid_bands(selected_genres):
    unique_bands = {}
    
    # 1. First, pull every artist from your provided SEED lists
    for genre in selected_genres:
        seeds = GENRE_SEEDS.get(genre, [])
        for seed_name in seeds:
            # Explicit search for seed names to get correct IDs/Thumbnails
            results = yt.search(seed_name, filter="artists", limit=1)
            if results:
                item = results[0]
                b_id = item['browseId']
                if b_id not in unique_bands:
                    unique_bands[b_id] = {
                        "name": item.get('artist') or item.get('title'),
                        "id": b_id,
                        "thumbnail": item['thumbnails'][-1]['url'] if 'thumbnails' in item else ""
                    }
                    print(f" [SEED] Loaded: {unique_bands[b_id]['name']}")

    # 2. Backfill only if we haven't reached 50 yet
    if len(unique_bands) < 50:
        fallbacks = ["top artists", "essentials", "hits"]
        for q_type in fallbacks:
            if len(unique_bands) >= 50: break
            for genre in selected_genres:
                query = f"{genre} {q_type}"
                results = yt.search(query, filter="artists", limit=20)
                for item in results:
                    b_id = item.get('browseId')
                    if b_id and b_id not in unique_bands:
                        unique_bands[b_id] = {
                            "name": item.get('artist') or item.get('title'),
                            "id": b_id,
                            "thumbnail": item['thumbnails'][-1]['url'] if 'thumbnails' in item else ""
                        }
                    if len(unique_bands) >= 50: break

    final_list = list(unique_bands.values())
    random.shuffle(final_list)
    return final_list[:50]



@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    selected_genres = data.get('genres', [])
    
    # This now handles the 50 count and duplicate removal in one go
    pool_of_50 = get_50_hybrid_bands(selected_genres)
    
    # If the user selected 70/30 split logic is a priority, 
    # we can sort the final 50 by popularity scores later.
    random.shuffle(pool_of_50)
    
    return jsonify(pool_of_50)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/select-twenty')
def select_twenty():
    return render_template('selection.html')

import sqlite3
import uuid # For generating unique share links

# Initialize Database
def init_db():
    try:
        conn = sqlite3.connect('rankings.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tiers 
                 (id TEXT PRIMARY KEY, data TEXT)''')
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Database error: {e}")

init_db()

@app.route('/save-tier', methods=['POST'])
def save_tier():
    ranking_data = request.json # This will be the JSON from your Tier List
    unique_id = str(uuid.uuid4())[:8] # Short unique ID
    
    conn = sqlite3.connect('rankings.db')
    c = conn.cursor()
    # We store the entire Tier JSON as a string
    import json
    c.execute("INSERT INTO tiers (id, data) VALUES (?, ?)", 
              (unique_id, json.dumps(ranking_data)))
    conn.commit()
    conn.close()
    
    return jsonify({"share_url": f"/view/{unique_id}"})


@app.route('/tier-list')
def tier_list():
    return render_template('tierlist.html')

@app.route('/view/<tier_id>')
def view_tier(tier_id):
    conn = sqlite3.connect('rankings.db')
    c = conn.cursor()
    c.execute("SELECT data FROM tiers WHERE id=?", (tier_id,))
    result = c.fetchone()
    conn.close()
    
    if result:
        # Pass the database string directly to the template
        return render_template('view_ranking.html', data=result[0])
    return "Ranking not found!", 404


import os

if __name__ == '__main__':
    # Use the port assigned by the cloud, or default to 5000 for local dev
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# if __name__ == '__main__':
#     app.run(debug=True)