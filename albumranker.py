import os
import random
#I uploaded a bunch of albums (some good some not-so-good) in albums.txt for testing. Change them if you want to rate your own
def load_albums(filename="albums.txt"):
    # Reads album names from a text file    
    with open(filename, "r", encoding="utf-8") as f:
        albums = [line.strip() for line in f if line.strip()]
    return albums

def ask_user(album_a, album_b, current_step, total_albums):
    # Asks the user to choose which album is better, with options to undo or pause
    while True:
        print(f"\n[Progress: Album {current_step}/{total_albums}]")
        print("Which album is better?")
        print(f"1: {album_a}")
        print(f"2: {album_b}")
        print("Options: Enter 'u' to restart this album, or 'p' to pause.")
        choice = input("Enter selection: ").strip().lower()
        
        if choice == '1':
            return "1"
        elif choice == '2':
            return "2"
        elif choice == 'u':
            return "undo"
        elif choice == 'p':
            return "pause"
        else:
            print("Invalid input. Please enter 1, 2, 'u', or 'p'.")

def print_current_standings(ranked_list):
    print("CURRENT STANDINGS:")
    for rank, album in enumerate(ranked_list, 1):
        print(f"{rank}. {album}")

def get_numerical_ratings(ranked_list):
    #rating system
    ratings = {}
    print("RATINGS (OUT OF 100)")
    print("="*45)
    print("Rate your albums from best to worst. You can edit any rating at the end.")
    
    i = 0
    while i < len(ranked_list):
        album = ranked_list[i]
        
        # Guide the user by showing the previous score if applicable
        context_str = ""
        if i > 0:
            prev_album = ranked_list[i-1]
            context_str = f" (Previous album '{prev_album}' was given a {ratings[prev_album]}/100)"

        score_input = input(f"\nRating for {album}{context_str}: ").strip()
        
        try:
            score = int(score_input)
            if 0 <= score <= 100:
                ratings[album] = score
                i += 1
            else:
                print("Please enter a score between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    # Edit Cycle Loop
    while True:
        print("REVIEW RATINGS")
        print("")
        for rank, album in enumerate(ranked_list, 1):
            print(f"{rank}. {album}: {ratings[album]}/100")
        
        edit_choice = input("Do you want to edit any rating? (yes/no): ").strip().lower()
        if edit_choice in ['no', 'n']:
            break
        elif edit_choice in ['yes', 'y']:
            try:
                rank_to_edit = int(input("Enter the rank number (#) you want to change: ").strip())
                if 1 <= rank_to_edit <= len(ranked_list):
                    album_to_edit = ranked_list[rank_to_edit - 1]
                    
                    while True:
                        new_score_input = input(f"Enter new score out of 100 for {album_to_edit}: ").strip()
                        try:
                            new_score = int(new_score_input)
                            if 0 <= new_score <= 100:
                                ratings[album_to_edit] = new_score
                                print(f"Updated {album_to_edit} to {new_score}/100.")
                                break
                            else:
                                print("Score must be between 0 and 100.")
                        except ValueError:
                            print("Please enter a valid whole number.")
                else:
                    print("Rank number out of range.")
            except ValueError:
                print("Invalid input. Please enter a valid rank number.")
        else:
            print("Invalid option. Type 'yes' or 'no'.")
            
    return ratings

def rank_albums():
    albums = load_albums()
    
    if not albums:
        print("No albums found.")
        return
    
    total_albums = len(albums)
    if total_albums == 1:
        print(f"\nFinal Ranked List:\n1. {albums[0]}")
        return
    random.shuffle(albums)

    # Start the ranked list with the first randomised album
    ranked_list = [albums[0]]
    
    # Process the remaining albums one by one
    i = 1
    early_exit = False
    
    while i < total_albums:
        current_album = albums[i]
        
        low = 0
        high = len(ranked_list) - 1
        insert_pos = 0
        restart_album = False
        
        # Binary insertion search loop
        while low <= high:
            mid = (low + high) // 2
            mid_album = ranked_list[mid]
            
            user_action = ask_user(current_album, mid_album, i + 1, total_albums)
            
            if user_action == "undo":
                print(f"Resetting placement search for: '{current_album}'")
                restart_album = True
                break 
                
            elif user_action == "pause":
                print_current_standings(ranked_list)
                print("PAUSED OPTIONS:")
                print("1. Resume ranking")
                print("2. End program completely right here and keep current list")
                pause_choice = input("Select 1 or 2: ").strip()
                
                if pause_choice == '2':
                    print("Ending ranking process early as requested.")
                    early_exit = True
                    break
                else:
                    print("Resuming...")
                    continue 
                
            elif user_action == "1":
                high = mid - 1
                insert_pos = mid
            elif user_action == "2":
                low = mid + 1
                insert_pos = low

        if early_exit:
            break
            
        if restart_album:
            continue
                
        ranked_list.insert(insert_pos, current_album)
        i += 1

    # Call Phase 2: Scoring the ranked list
    album_ratings = get_numerical_ratings(ranked_list)

    # Final Output Phase
    print("FINAL ALBUM STANDINGS")
    for rank, album in enumerate(ranked_list, 1):
        print(f"{rank}. {album} - {album_ratings[album]}/100")

if __name__ == "__main__":
    rank_albums()
