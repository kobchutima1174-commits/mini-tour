from flask import Flask, render_template
import folium

app = Flask(__name__)

# 1. ข้อมูลสถานที่ท่องเที่ยว (Kanchanaburi One Day Trip)
locations = [
    {
        "id": 1,
        "name": "อุทยานแห่งชาติเขาแหลม",
        "lat": 15.1010826580672,
        "lng": 98.7940648371254,
        "description": "ดินแดนแห่งผืนป่าตะวันตกอันอุดมสมบูรณ์ ไฮไลท์คือสะพานไม้อุตตมานุสรณ์ และจุดชมวิวป้อมปี่ที่สามารถมองเห็นวิวพระอาทิตย์ตกดินเหนืออ่างเก็บน้ำเขื่อนวชิราลงกรณได้อย่างสวยงามตระการตา",
        "image_url": "https://images.unsplash.com/photo-1589308078059-be1415eab4c3?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 2,
        "name": "อุทยานแห่งชาติไทรโยค",
        "lat": 14.508931824691606,
        "lng": 98.98357900494995,
        "description": "อุทยานประวัติศาสตร์และธรรมชาติ เลื่องชื่อจาก 'น้ำตกไทรโยคใหญ่' ที่ไหลดิ่งลงสู่แม่น้ำแควแควน้อยอย่างมีเอกลักษณ์ เหมาะสำหรับการล่องแพเปียก สัมผัสอากาศบริสุทธิ์และไอเย็นจากสายน้ำ",
        "image_url": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 3,
        "name": "อุทยานแห่งชาติเอราวัณ",
        "lat": 14.426487828764621,
        "lng": 99.28295643143015,
        "description": "ผืนป่าอนุรักษ์ขนาดใหญ่ที่เป็นต้นกำเนิดของน้ำตกเอราวัณ รายล้อมด้วยเส้นทางศึกษาธรรมชาติที่สมบูรณ์ มีจุดเด่นด้านความหลากหลายทางชีวภาพและทัศนียภาพของป่าเบญจพรรณ",
        "image_url": "https://images.unsplash.com/photo-1546708973-b339540b5162?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 4,
        "name": "เขื่อนศรีนครินทร์",
        "lat": 14.412508671129645,
        "lng": 99.14583856749876,
        "description": "เขื่อนอเนกประสงค์ขนาดใหญ่บนแควใหญ่ วิวทิวทัศน์รอบอ่างเก็บน้ำโอบล้อมด้วยขุนเขา มีจุดชมวิวสันเขื่อนที่กว้างขวาง เหมาะแก่การมาพักผ่อนหย่อนใจและชมทัศนียภาพมุมสูง",
        "image_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 5,
        "name": "น้ำตกเอราวัณ",
        "lat": 14.36289162990611,
        "lng": 99.1502339099092,
        "description": "น้ำตกหินปูนชื่อดังที่มีความยาวถึง 7 ชั้น โดดเด่นด้วยน้ำสีเขียวมรกตใสสะอาดจนเห็นตัวปลา โดยเฉพาะชั้นที่ 7 ที่มีลักษณะคล้ายหัวช้างเอราวัณสามเศียร ซึ่งเป็นที่มาของชื่อน้ำตก",
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80"
    }
]

@app.route('/')
def index():
    # 2. เริ่มต้นสร้างแผนที่ Folium (กำหนดจุดกึ่งกลางที่ กาญจนบุรี)
    start_coords = [14.5, 99.0]
    my_map = folium.Map(
        location=start_coords, 
        zoom_start=9, 
        tiles="CartoDB positron" # เลือกแผนที่โทนคลีนๆ เพื่อให้เข้ากับ UI ของเว็บ
    )
    
    # 3. ลูปเพิ่ม Markers ลงบนแผนที่ พร้อม Popup สวยงาม
    for loc in locations:
        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={loc['lat']},{loc['lng']}"
        popup_html = f"""
        <div style="font-family: 'Prompt', sans-serif; width: 200px;">
            <strong style="color: #2d3748;">{loc['name']}</strong><br>
            <p style="font-size: 12px; margin: 5px 0; color: #718096;">{loc['description'][:50]}...</p>
            <a href="{gmaps_url}" target="_blank" style="display: inline-block; padding: 5px 10px; background-color: #4a5568; color: white; text-decoration: none; border-radius: 5px; font-size: 11px;">เปิด Google Maps</a>
        </div>
        """
        folium.Marker(
            location=[loc['lat'], loc['lng']],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=loc['name'],
            icon=folium.Icon(color="teal", icon="info-sign")
        ).add_to(my_map)
        
    # แปลงแผนที่ Folium เป็น HTML String
    map_html = my_map._repr_html_()
    
    return render_template('index.html', locations=locations, map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)