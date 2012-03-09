import xml.etree.ElementTree as ET

class Coordinate(object):
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return "{},{}".format(self.longitude, self.latitude)

class LineString(object):
    def __init__(self, name, style, coordinates):
        self.style = style
        self.coordinates = coordinates
        self.name = name

    def write(self, parent):
        placemark = ET.SubElement(parent, "Placemark")
        ET.SubElement(placemark, "name").text = self.name
        ET.SubElement(placemark, "styleUrl").text = "#{0}".format("style_" + self.style.id)
        line = ET.SubElement(placemark, "LineString")
        ET.SubElement(line, "tessellate").text = "1"
        ET.SubElement(line, "coordinates").text = " ".join(map(str, self.coordinates))

class Style(object):
    def __init__(self, id, *substyles):
        self.id = id
        self.substyles = substyles

    def write(self, parent):
        style_element = ET.SubElement(parent, "Style")
        style_element.set("id", "style_" + self.id)
        for substyle in self.substyles:
            substyle.write(style_element)

    def __eq__(self, other):
        if not other.__class__ == self.__class__:
            return False
        return other.id == self.id

    def __ne__(self, other):
        return not self.__eq__(other)

class IconStyle(object):
    def __init__(self, url, hotspot_x="0.5", hotspot_y="1.0"):
        self.id = id
        self.url = url
        self.hotspot_x = hotspot_x
        self.hotspot_y = hotspot_y

    def write(self, parent):
        icon_style = ET.SubElement(parent, "IconStyle")
        icon = ET.SubElement(icon_style, "Icon")
        ET.SubElement(icon, "href").text = self.url
        hotspot = ET.SubElement(icon_style, "hotSpot")
        hotspot.set("x", self.hotspot_x)
        hotspot.set("y", self.hotspot_y)
        hotspot.set("xunits", "fraction")
        hotspot.set("yunits", "fraction")

class LineStyle:
    def __init__(self, color, width):
        self.color = color
        self.width = width

    def write(self, parent):
        line_style = ET.SubElement(parent, "LineStyle")
        ET.SubElement(line_style, "color").text = self.color
        ET.SubElement(line_style, "colorMode").text = "normal"
        ET.SubElement(line_style, "width").text = str(self.width)
        

class Place(object):
    def __init__(self, name, description, point, style, folder=None):
        if not folder:
            folder = 'Placemarks'
        self.name = name
        self.description = description
        self.point = point
        self.style = style
        self.folder = folder

    def write(self, parent):
        placemark = ET.SubElement(parent, "Placemark")
        ET.SubElement(placemark, "name").text = self.name
        ET.SubElement(placemark, "description").text = self.description
        ET.SubElement(placemark, "styleUrl").text = "#{0}".format("style_" + self.style.id)
        point = ET.SubElement(placemark, "Point")
        ET.SubElement(point, "coordinates").text = str(self.point)

class Kml(object):
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
        self.places = []
        self.lines = []

    def to_string(self):
        root = ET.Element("kml")
        root.set("xmlns", "http://www.opengis.net/kml/2.2")
        document = ET.SubElement(root, "Document") 
        ET.SubElement(document, "name").text = self.name
        if self.description:
            ET.SubElement(document, "description").text = self.description

        styles = []
        for place in self.places:
            if not place.style in styles:
                styles.append(place.style)

        for line in self.lines:
            if not line.style in styles:
                styles.append(line.style)
    
        for style in styles:
            style.write(document)

        for line in self.lines:
            line.write(document)

        folders = {}
        folders[""] = document
        for folder_name in sorted(set([pm.folder for pm in self.places])):
            #folder = ET.SubElement(document, "Folder")
            path = folder_name.split("/")
            for i in range(len(path)):
                partial_path = "/".join(path[:i + 1])
                if partial_path not in folders:
                    parent_folder = folders["/".join(path[:i])]
                    folder = ET.SubElement(parent_folder, "Folder")
                    ET.SubElement(folder, "name").text = path[i].split("|")[-1]
                    ET.SubElement(folder, "open").text = "0" if i > 0 else "1"
                    ET.SubElement(folder, "visibility").text = "1"
                    folders[partial_path] = folder
                     
                
            
            #folder.set("id", "f{0:05d}".format(n))
            folder = folders["/".join(path)]
            
            for place in [pm for pm in self.places if pm.folder == folder_name]:
                place.write(folder)

        return '<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(root)




    
