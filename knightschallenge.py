import requests

def maketribes(alliances):
    tribes = []

    def find_tribe(wizard):
        for tribe in tribes:
            if wizard in tribe:
                return tribe
        return None
    
    def add_to_tribe(wiz1, wiz2):
        tribe1 = find_tribe(wiz1)
        tribe2 = find_tribe(wiz2)

        if tribe1 is None and tribe2 is None:
            tribes.append([wiz1, wiz2])
        elif tribe1 is not None and tribe2 is None:
            tribe1.append(wiz2)
        elif tribe1 is None and tribe2 is not None:
            tribe2.append(wiz1)
        elif tribe1 != tribe2:
            tribe1.extend(tribe2)
            tribes.remove(tribe2)

    for alliance in alliances:
        wizard1, wizard2 = alliance
        add_to_tribe(wizard1, wizard2)

    return tribes
url = 'https://artemis.hackillinois.org/challenge'

jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImdpdGh1YjE0MDY0OTA4NCIsImVtYWlsIjpudWxsLCJwcm92aWRlciI6ImdpdGh1YiIsInJvbGVzIjpbIlVTRVIiXSwiZXhwIjoxNzEwNzMyMDI3Ljk2NiwiaWF0IjoxNzA4MTQwMDI3fQ.9Yug4YPevmSty5kbZaKYu35BWDI1sPwtjkgXw-KsClY"

headers = {
    "Authorization": jwt_token,
    "Content-Type": "application/json"
}

def getscores(tribes):
    scores = []
    for tribe in tribes:
        sum = 0
        for wiz in tribe:
            sum += wizards[wiz]
        scores.append(sum)
    return scores
            

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        wizards = data['wizards']
        alliances = data['alliances']
        tribes = maketribes(alliances)
        tribescores = getscores(tribes)
        max_goodness = max(tribescores)
        postdata = {
            "max_goodness": max_goodness
        }
        
        try:
            postresponse = requests.post(url, headers=headers, json=postdata)
            
            if postresponse.status_code == 200:
                print("Solution submitted successfully!")
            else:
                print(f"Failed to submit solution. Status code: {postresponse.status_code}")
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        
except Exception as e:
    print(f"An error occurred: {str(e)}")
