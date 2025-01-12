import os
import requests
from croniter import croniter
from datetime import datetime
import time

#Bazarr Information
BAZARR_HOSTNAME = os.environ.get('BAZARR_HOSTNAME', 'localhost')
BAZARR_PORT = os.environ.get('BAZARR_PORT', '6767')
BAZARR_APIKEY = os.environ.get('BAZARR_APIKEY', '')

CRON_SCHEDULE = os.environ.get('CRON_SCHEDULE', '*/5 * * * *')

FIRST_LANG = os.environ.get('FIRST_LANG', 'pl')
#Secondary language preference code2. Leave empty ('') if do not have secondary preference
SECOND_LANG = os.environ.get('SECOND_LANG', '')

HEADERS = {'Accept': 'application/json', 'X-API-KEY': BAZARR_APIKEY}

def translate_episode_subs():
    #List wanted episodes
    wanted_episodes_resp = requests.get(f"http://{BAZARR_HOSTNAME}:{BAZARR_PORT}/api/episodes/wanted?start=0&length=-1",headers=HEADERS)
    if wanted_episodes_resp.status_code == 200:
        wanted_episodes = wanted_episodes_resp.json()
        if wanted_episodes['total'] > 0:
            for episode in wanted_episodes['data']:
                found = False
                sonarrSeriesId = episode['sonarrSeriesId']
                sonarrEpisodeId = episode['sonarrEpisodeId']
                #Download FIRST_LANG subtitles
                down_ep_resp_first = requests.patch(f"http://{BAZARR_HOSTNAME}:{BAZARR_PORT}/api/episodes/subtitles?seriesid={sonarrSeriesId}&episodeid={sonarrEpisodeId}&language={FIRST_LANG}&forced=false&hi=false",headers=HEADERS)
                if down_ep_resp_first.status_code == 204: 
                    found = True
                if SECOND_LANG != '':
                    #Download SECOND_LANG subtitles
                    down_ep_resp_sec = requests.patch(f"http://{BAZARR_HOSTNAME}:{BAZARR_PORT}/api/episodes/subtitles?seriesid={sonarrSeriesId}&episodeid={sonarrEpisodeId}&language={SECOND_LANG}&forced=false&hi=false",headers=HEADERS)
                    if down_ep_resp_sec.status_code == 204: 
                        found = True
                if not found:
                    #Download English subtitles
                    down_ep_en_resp = requests.patch(f"http://{BAZARR_HOSTNAME}:{BAZARR_PORT}/api/episodes/subtitles?seriesid={sonarrSeriesId}&episodeid={sonarrEpisodeId}&language=en&forced=false&hi=false",headers=HEADERS)
                    if down_ep_en_resp.status_code == 204:
                        print("EN episode subtitles downloaded/imported for {series} {episode}.".format(series=episode['seriesTitle'],episode=episode['episode_number']))
                        subs_path = ""
                        #Get episode history
                        ep_hist_resp = requests.get(f"http://{BAZARR_HOSTNAME}:{BAZARR_PORT}/api/episodes/history?start=0&length=-1&episodeid={sonarrEpisodeId}",headers=HEADERS)
                        if ep_hist_resp.status_code == 200:
                            ep_history = ep_hist_resp.json()
                            #Get most recent download
                            for download in ep_history['data']:
                                if download['action'] == 1:
                                    subs_path = download['subtitles_path']
                                    break
                        if subs_path != "":
                            ep_trans_resp = requests.patch(f"http://{BAZARR_HOSTNAME}:{BAZARR_PORT}/api/subtitles?action=translate&language={FIRST_LANG}&path={subs_path}&type=episode&id={sonarrEpisodeId}&forced=false&hi=false&original_format=true",headers=HEADERS)
                            if ep_trans_resp.status_code == 204:
                                print("{series} {episode} subtitles translated to {lang}!".format(series=episode['seriesTitle'],episode=episode['episode_number'],lang=FIRST_LANG))
                            else:
                                print("{series} {episode} subtitles translation to {lang} failed!".format(series=episode['seriesTitle'],episode=episode['episode_number'],lang=FIRST_LANG))
                    else:
                        print("No EN subtitles downloaded/imported for {series} {episode}.".format(series=episode['seriesTitle'],episode=episode['episode_number']))
                else:
                    print("{series} {episode} subtitles downloaded/imported direcly!".format(series=episode['seriesTitle'],episode=episode['episode_number']))
        else:
            print("No episode subtitles wanted.")
            
def translate_movie_subs():
    #List wanted episodes
    wanted_movies_resp = requests.get(f"http://{BAZARR_HOSTNAME}:{BAZARR_PORT}/api/movies/wanted?start=0&length=-1",headers=HEADERS)
    if wanted_movies_resp.status_code == 200:
        wanted_movies = wanted_movies_resp.json()
        if wanted_movies['total'] > 0:
            for movie in wanted_movies['data']:
                found = False
                radarrId = movie['radarrId']
                #Download FIRST_LANG subtitles
                down_mov_resp_first = requests.patch(f"http://{BAZARR_HOSTNAME}:{BAZARR_PORT}/api/movies/subtitles?radarrid={radarrId}&language={FIRST_LANG}&forced=false&hi=false",headers=HEADERS)
                if down_mov_resp_first.status_code == 204: 
                    found = True
                if SECOND_LANG != '':
                    #Download SECOND_LANG subtitles
                    down_mov_resp_sec = requests.patch(f"http://{BAZARR_HOSTNAME}:{BAZARR_PORT}/api/movies/subtitles?radarrid={radarrId}&language={SECOND_LANG}&forced=false&hi=false",headers=HEADERS)
                    if down_mov_resp_sec.status_code == 204: 
                        found = True
                if not found:
                    #Download English subtitles
                    down_mov_resp = requests.patch(f"http://{BAZARR_HOSTNAME}:{BAZARR_PORT}/api/movies/subtitles?radarrid={radarrId}&language=en&forced=false&hi=false",headers=HEADERS)
                    if down_mov_resp.status_code == 204:
                        print("EN subtitles downloaded/imported for {movie}.".format(movie=movie['title']))
                        subs_path = ""
                        #Get movie history
                        mov_hist_resp = requests.get(f"http://{BAZARR_HOSTNAME}:{BAZARR_PORT}/api/movies/history?start=0&length=-1&radarrid={radarrId}",headers=HEADERS)
                        if mov_hist_resp.status_code == 200:
                            mov_history = mov_hist_resp.json()
                            #Get most recent download
                            for download in mov_history['data']:
                                if download['action'] == 1:
                                    subs_path = download['subtitles_path']
                                    break
                        if subs_path != "":
                            mov_trans_resp = requests.patch(f"http://{BAZARR_HOSTNAME}:{BAZARR_PORT}/api/subtitles?action=translate&language={FIRST_LANG}&path={subs_path}&type=movie&id={radarrId}&forced=false&hi=false&original_format=true",headers=HEADERS)
                            if mov_trans_resp.status_code == 204:
                                print("{movie} subtitles translated to {lang}!".format(movie=movie['title'],lang=FIRST_LANG))
                            else:
                                print("{movie} subtitles translation to {lang} failed!".format(movie=movie['title'],lang=FIRST_LANG))
                    else:
                        print("No EN subtitles downloaded/imported for {movie}.".format(movie=movie['title']))
                else:
                    print("{movie} subtitles downloaded/imported directly!".format(movie=movie['title']))
        else:
            print("No movie subtitles wanted.")
            
def main():
    translate_movie_subs()
    translate_episode_subs()

def get_next_run():
    """Calculate the next run time based on cron schedule."""
    iter = croniter(CRON_SCHEDULE, datetime.now())
    return iter.get_next(datetime)


if __name__ == "__main__":
    # Main loop with cron scheduling
    while True:
        next_run = get_next_run()
        now = datetime.now()
        wait_seconds = (next_run - now).total_seconds()
        print(f'Next run scheduled at {next_run.strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'Waiting for {int(wait_seconds)} seconds...')
        time.sleep(wait_seconds)
        print('Starting the translate...')
        main()