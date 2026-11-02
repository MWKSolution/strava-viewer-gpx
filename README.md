# Strava-Viewer...  
### **...for viewing simple summaries of recorded Strava activities using  [Dash](https://dash.plotly.com) framework.**  
Since June 2026 [Strava API](https://developers.strava.com) is not available for non-subscription users. This new version is based on downloaded **GPX** files from [Strava](strava.com) app.  
To make it easier using *Chrome extension* [Strava Bulk GPX Export](https://chromewebstore.google.com/detail/strava-bulk-gpx-export/nabkcpkedegngoebodobopcojpahgbba) is strongly recommended.  
Manually entered activities which don't have **GPX** traces can be loaded using **activities.csv** file from downloaded account.
---

### Using Strava-Viewer app

1. Use *Chrome extension* ***Strava Bulk GPX Export*** to download *GPX* traces of your activities. Copy them to **/gpx** directory. (*there is a daily limit for bulk download*)   
2. Click **Load data GPX**. This will create or update **activities.json** file. Any duplicates of activities will not be loaded.
3. Manually entered activities generally canot be downloaded using ***Strava Bulk GPX Export*** - sometimes they appear as *GPX* file, but they are not valid *GPX* files.
4. Change your account language to *english* for downloading to comply with the rest of the data.  
5. Download your strava account. Copy **activities.csv** file to **/csv** directory. (*can be done only once a week*)   
6. Click **Load data CSV**. Non-duplicated manually entered activities will be added to database.  
7. Gradually add new activities as they appear and run app.  

**! Please check console log for any errors during loading !**  
*Please note: When first used, app has an empty dashboard and activities.json file doesn't exist* 

---

