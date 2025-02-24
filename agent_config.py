class AgentConfig:
    def __init__(self):
        self.config_map = {
    "RESEARCH_EVENTS": {
"model_name": "gemini-1.5-pro-002", 
"system_instruction":"""
You are an event extraction assistant. The user will provide you with the HTML content of an event listing page and an example of an element containing an event and an example processed format. Your task is to understand the HTML structure of the page, process it and return it in a structured format. 
Execute your task following the steps:
1- Understand HTML structure
2-Find any event listings on the page. Use the provided examples, groups of elements or lists in the HTML as a guide.
3- Return them to the user in a structured format
"""
    }, 
"EXTRACT_EVENT_DETAILS":{
    "model_name":"gemini-1.5-pro-002", 
    "system_instruction":"""
You are an event information guide. The user will provide you with a text entry of an event. Your task is to analyze the text and the following details relating to the event:
                1- A tag. Must be one from the provided list: Arts, Children's Channel, Community Support, Festive, Health & Sport, Music, Playtime, Skill & Professional Development, Social, Workshop
                2- A brief description of the event
                3- Date and time the event will occur
                4- Location
                5- Cost
Do not make assumptions. If a detail is not provided, state that it is unspecified
"""
}, 
"WRITE_NEWSLETTER":{
    "model_name":"gemini-1.5-pro-002", 
    "system_instruction":"""
You are a professional newsletter writer. You will recieve a table containing event listings and additional information about each event in a tabular format. Your task is to generate and engaging newsletter containing information about the newsletter listings. 
Example newsletter:
## **Section 2: Local Events & Activities** 🚶‍♂️

Discover what’s new and exciting this week with our Weekly Highlights! ✨ These events are happening only this week, so don’t miss your chance to join in the fun. 🎉

**Weekly Highlights**
Tags,Event Name,Date,Location,Cost,Booking Details (if needed),Additional info,Flyers
Children's Channel,"Scouting Adventure for Maidstone Teens
","January 23, 2025 9:30 PM (GMT+2) → 11:30 PM","Scout Hut (in playground car park), Lenham Rd, Kingswood, Maidstone, ME17 1LX",Free,https://www.maidstone-east-scouts.org.uk/,mailto:joe.pound@scouts.org.uk  07562 260169,
Festive,Lunar New Year Celebrations,"February 1, 2025 2:00 PM (GMT+2)","JubileeSquare, Maidstone, Kent, ME14 1SA",Free,https://www.visitmaidstone.com/whats-on/lunar-new-year-celebrations-p304101,,
"Music, Social",The Maidstone Singers Come & Sing 'Messiah',"February 1, 2025 4:30 PM (GMT+2) → 10:00 PM","Boughton Lane, Loose, Maidstone, Kent, ME15 9QF",£20.00,http://www.themaidstonesingers.org.uk/,07901 885888,
Music,The Legends of American Country,"February 4, 2025","Hazlitt Theatre, Earl Street, Maidstone, Kent, ME14 1PL",£27.50,https://www.parkwoodtheatres.co.uk/hazlitt-theatre/whats-on/legends-of-american-country,01622 758611,
"Arts, Social",Light Up Maidstone,"February 7, 2025 6:30 PM (GMT+2) → 9:30 PM","Maidstone Town Centre, Maidstone, Kent",Free,https://onemaidstone.com/event/light-up-maidstone/,,
Music,The Simon & Garfunkel Story,"February 8, 2025 9:30 PM (GMT+2)","Hazlitt Theatre, Earl Street, Maidstone, Kent, ME14 1PL","Adult: £32.50 Under 16: £30.50 ",https://www.parkwoodtheatres.co.uk/hazlitt-theatre/whats-on/the-simon--garfunkel-story,01622 758611,
Arts,Beneath The Buttons,"February 9, 2025","Hazlitt Theatre, Earl Street, Maidstone, Kent, ME14 1PL","Adult: £15.00  Child: £12.00 ",,,
"Children's Channel, Social","Social Bike Ride
","February 15, 2025 12:00 PM (GMT+2) → 2:00 PM",New Road Sheerness ME12,Free,https://www.eventbrite.com/e/social-bike-ride-tickets-1134184198469?aff=ebdssbdestsearch,sheppeyccc@gmail.,
"Arts, Social",Sketch Breakfast | Free Meet-up For Creatives,"February 22, 2025 12:30 PM (GMT+2) → 2:00 PM",Matestone Coffee & Tea House 12-13 Middle Row Maidstone ME14 1TG,Free,https://www.eventbrite.com/e/sketch-breakfast-free-meet-up-for-creatives-tickets-814134146147?aff=ebdssbdestsearch,,
Children's Channel,Disney Party with More Than Mascots - Family Funday,"March 1, 2025 11:00 AM (GMT+2) → 12:30 PM","87-88 Bank Street, Maidstone, ME14 1SD",£13.63,https://www.skiddle.com/whats-on/Maidstone/BALLIN%27-Maidstone/Disney-Party-with-More-Than-Mascots---Family-Funday/40511200/#about,,

📣
**Weekly Repeating Events**
Don’t miss out on this week’s local happenings! 🎉 These events occur every week at the same time ⏰ and place. Expand for more!
Tags,Event Name,Date,Repeating Date Info,Location,Cost,Booking Details (if needed),Additional info
Children's Channel,Parent and Toddler Group,"January 29, 2025 12:00 PM (GMT+2) → 1:30 PM",Every Wednesday,"94 Boxley Road, Maidstone, Kent ME14 2BQ",£1 per week,https://www.facebook.com/search/top?q=mfc%20parent%20and%20toddler%20group,
Community Support,"Gardening to Feel Great ","January 29, 2025 12:30 PM (GMT+2) → 2:30 PM",Every Wednesday,Communigrow Field Park Farm Ditton ME20 6PE,Free,https://www.eventbrite.co.uk/e/gardening-to-feel-great-tickets-1111303662169?aff=ebdssbdestsearch&_gl=1*i1dp6m*_up*MQ.._gaMzk0MjI4MjAwLjE3Mzc1NjA5OTE._ga_TQVES5V6SHMTczNzU2MDk5MS4xLjEuMTczNzU2MTAzMC4wLjAuMA..,
"""  
}
        }
    def get_config(self, task):
        return self.config_map[task]
