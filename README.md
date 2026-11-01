# Strava-Viewer...  
### **...for viewing simple summaries of recorded Strava activities using  [Dash](https://dash.plotly.com) framework.**  
Since June 2026 [Strava API](https://developers.strava.com) is not available for non-subscription users so this new version is based on downloaded **GPX** files from [Strava](strava.com) app.  
To make it easier using *Chrome extension* [Strava Bulk GPX Export](https://chromewebstore.google.com/detail/strava-bulk-gpx-export/nabkcpkedegngoebodobopcojpahgbba) is strongly recommended.  
Saving data to Redis database is also dropped and now only saving to local file (**activities.json**) is possible.
---

### Strava-Viewer app

Some simple summaries of activities data are presented using  **[Dash](https://dash.plotly.com)** framework.  
Click **Load data**. This will create or update **activities.json** file. Any duplicates of activities will be dropped.  
Please note: When first used, app has an empty dashboard.  

---

