# -*- coding: utf-8 -*-
"""Build the 24 Nov 2026 front page: dotted world map + HTML."""
import json, os
from PIL import Image, ImageDraw

W, H = 470, 240          # map panel css size
S = 2                    # supersample
LAT_TOP, LAT_BOT = 84, -58

STORIES = [
 # id, place, region, section, status, headline, detail, source, lon, lat
 (1,"Strait of Hormuz","Middle East","Energy war","CLAIM",
  "Three tankers burn on mines as the US blockade closes in",
  "IRGC says the ships hit naval mines under US escort; Tehran vows to break the blockade by all means.",
  "Al Jazeera",56.5,26.6),
 (2,"Gulf of Sirte","Africa","Ukraine war","REPORTED",
  "Ukrainian drones sink Russian warships off Libya",
  "Zelenskyy posts strike video from 2,000 km away; Kremlin says trilateral talks may go to Abu Dhabi.",
  "AP · Kyiv",18.5,31.0),
 (3,"Antalya","Europe","Climate","REPORTED",
  "COP31 ends with no pact, the first since 2009",
  "Final text drops any mention of fossil fuels; EU refuses to adopt it.",
  "UN News",30.7,36.9),
 (4,"Washington","Americas","Politics","REPORTED",
  "Trump urges faster federal executions",
  "Attacks Newsom over 548 commutations as the White House pushes a harder line on capital cases.",
  "Al Jazeera",-77.0,38.9),
 (5,"Santa Clara","Americas","Technology","REPORTED",
  "Nvidia reinstates Jensen Huang as CEO",
  "Board reverses itself days after an affair scandal; shares jump 31% and Trump claims credit.",
  "Reuters · AP",-121.96,37.35),
 (6,"Serang","Asia","Disaster","ONGOING",
  "Candy factory fire: 26 body bags recovered",
  "Blaze at the Banten plant burned for hours; dozens of workers still unaccounted for.",
  "Antara",106.15,-6.12),
 (7,"Seoul","Asia","Security","REPORTED",
  "Russian warplanes enter Korea's air zone",
  "Jets scrambled and an island alert issued; Seoul says airspace was not violated.",
  "Yonhap",126.98,37.57),
 (8,"Khartoum","Africa","Conflict","REPORTED",
  "Drone strikes hit Sudan's capital, UN building damaged",
  "The UN condemned the strikes, which it suspects came from Ethiopia.",
  "AP",32.5,15.5),

 (9,"Brussels","Europe","Labour","ONGOING",
  "General strike grounds Belgium's flights","Brussels and Charleroi shut as unions fight austerity.","BBC",4.35,50.85),
 (10,"Manchester","Europe","Emergency","REPORTED",
  "12,000 flee Co-op Live after substance released","Arena evacuated mid-show; cause still unclear.","BBC",-2.24,53.48),
 (11,"Berlin","Europe","Security","REPORTED",
  "Hundreds of German schools get bomb threats","Evacuations across several states; police see no concrete danger.","Xinhua",13.4,52.5),
 (12,"Iowa","Americas","Politics","REPORTED",
  "Court clears Army's Iowa explosives burn","Appeals court lifts the hold on detonating unstable munitions.","Forbes",-93.6,41.6),
 (13,"Washington","Americas","Trade","REPORTED",
  "US blacklists Megaspeed over export controls","Chip broker added amid the Nvidia controversy.","CNBC",-77.0,38.9),
 (14,"Jakarta","Asia","Politics","REPORTED",
  "Prabowo names two vice-presidential picks","Speaker announces Amran Sulaiman and Sugiono.","Antara",106.85,-6.2),
 (15,"Pyongyang","Asia","Diplomacy","REPORTED",
  "Kim Yo-jong threatens to shut Swiss office","Retaliation for sanctions on a children's camp.","Yonhap",125.75,39.03),
 (16,"Singapore","Asia","Economy","REPORTED",
  "GDP grows 6.1%, 2026 forecast raised","Trade ministry credits AI demand.","CNA",103.8,1.35),
 (17,"Tokyo","Asia","Politics","REPORTED",
  "Opposition moves to censure a scandal-hit minister","Motion filed as the cabinet's ratings slide.","Nikkei",139.7,35.68),
 (18,"Beijing","Asia","Diplomacy","REPORTED",
  "China protests Colombian lawmakers' Taiwan visit","Beijing says the trip violates its sovereignty.","Global Times",116.4,39.9),
 (19,"Abuja","Africa","Economy","REPORTED",
  "Oil output falls short of the 1.84m bpd target","Revenue at risk as production lags the budget.","The Sun",7.5,9.06),
 (20,"Nairobi","Africa","Climate","REPORTED",
  "World Bank warns El Nino brings floods and drought","East Africa faces floods, the south a dry spell.","World Bank",36.8,-1.3),
 (21,"Canberra","Oceania","Diplomacy","REPORTED",
  "Australia and Singapore deepen AI and supply ties","Albanese and Wong meet for annual leaders' talks.","Xinhua",149.1,-35.3),
 (22,"Canberra","Oceania","Technology","REPORTED",
  "Greens win billions in fines for big tech","Digital duty of care passes with heavy penalties.","Guardian",149.1,-35.3),
 (23,"Geneva","Europe","Sport","REPORTED",
  "Youngest world chess title match opens","Gukesh and Sindarov, both 20, start in Cologny.","The Hindu",6.14,46.2),
 (24,"Athens","Europe","Culture","REPORTED",
  "Acropolis Museum reopens after seven years","Greece's oldest museum returns to the public.","TOI",23.73,37.98),
 (25,"Hodeidah","Middle East","Conflict","REPORTED",
  "Strikes on Yemen telecom sites kill 17","Houthi media blames Saudi warplanes; 11 wounded.","Xinhua",42.95,14.8),
 (26,"Khan Younis","Middle East","Conflict","REPORTED",
  "Drone strike on a Gaza police post kills three","Five wounded, medics at al-Nasser hospital say.","Al Jazeera",34.3,31.35),
 (27,"Lahj","Middle East","Conflict","CLAIM",
  "Houthis say they downed a Wing Loong II","The armed drone fell off Bab al-Mandeb, the group says.","Al Jazeera",44.9,13.1),
 (28,"New York","Americas","Markets","REPORTED",
  "Wall Street's best day in months","S&P 500 +4.84%, Dow +3.01% to 49,595 on the Nvidia reversal.","Reuters",-74.0,40.7),
 (29,"World","World","Markets","REPORTED",
  "Oil at a three-month low, gold off its floor","Brent $88.97 and WTI $79.94 as supply fears fade.","Reuters",None,None),
]

REGIONS = [("Europe","#1F4E9C"),("Middle East","#B3202C"),("Africa","#1E7A4B"),
           ("Asia","#C0661A"),("Americas","#5B3E96"),("Oceania","#0E6E77"),("World","#333A45")]


def project(lon, lat):
    x = (lon + 180.0) / 360.0 * W * S
    y = (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * H * S
    return x, y


def build_map(out_png):
    geo = json.load(open('/root/.hermes/cache/scratch/world_land.geojson'))
    mask = Image.new('L', (W * S, H * S), 0)
    d = ImageDraw.Draw(mask)
    for feat in geo['features']:
        g = feat['geometry']
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in polys:
            ring = [project(lon, lat) for lon, lat in poly[0]]
            if len(ring) > 2:
                d.polygon(ring, fill=255)
    img = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    px = img.load()
    step = 4 * S
    for y in range(step // 2, H * S, step):
        for x in range(step // 2, W * S, step):
            if mask.getpixel((x, y)) > 0:
                r = int(1.35 * S)
                for dy in range(-r, r + 1):
                    for dx in range(-r, r + 1):
                        if dx * dx + dy * dy <= r * r:
                            xx, yy = x + dx, y + dy
                            if 0 <= xx < W * S and 0 <= yy < H * S:
                                px[xx, yy] = (110, 118, 132, 235)
    img.resize((W, H), Image.LANCZOS).save(out_png)
    return img.size


if __name__ == '__main__':
    print(build_map('/root/.hermes/cache/scratch/poster2/map.png'))
    print(len(STORIES), "stories")
