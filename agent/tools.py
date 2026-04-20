"""
Agent tools — each tool handles a specific domain of Ladakh travel knowledge.
"""

import json
import os
from pathlib import Path
from langchain_core.tools import tool
from utils.weather import get_weather_for_location

DATA_DIR = Path(__file__).parent.parent / "data"


def _load_json(filename: str) -> dict:
    """Load a JSON data file."""
    filepath = DATA_DIR / filename
    with open(filepath, "r") as f:
        return json.load(f)


@tool
def check_permit_requirements(query: str) -> str:
    """Check Inner Line Permit (ILP) requirements for visiting specific areas in Ladakh.
    Use this when the user asks about permits, ILP, or entry requirements.
    Input should be the area or region they want to visit."""
    
    data = _load_json("permits.json")
    
    query_lower = query.lower()
    results = []
    
    for area, info in data["areas"].items():
        if any(keyword in query_lower for keyword in info.get("keywords", [area.lower()])):
            result = f"**{area}**\n"
            result += f"- Permit required: {info['permit_required']}\n"
            result += f"- How to apply: {info['how_to_apply']}\n"
            result += f"- Cost: {info['cost']}\n"
            result += f"- Processing time: {info['processing_time']}\n"
            result += f"- Validity: {info['validity']}\n"
            if info.get("notes"):
                result += f"- Notes: {info['notes']}\n"
            results.append(result)
    
    if not results:
        return (
            "For most areas in Ladakh (outside Leh city), Indian nationals need an "
            "Inner Line Permit (ILP). Foreign nationals need a Protected Area Permit (PAP). "
            "You can apply online at https://www.lahdclehpermit.in or at the DC Office in Leh. "
            "Cost is typically ₹400-600 for Indians. Processing takes 1-3 hours online."
        )
    
    return "\n".join(results)


@tool
def get_weather_info(location: str) -> str:
    """Get current weather and forecast for a Ladakh location.
    Use this when the user asks about weather, temperature, or conditions.
    Input should be the location name (e.g., 'Leh', 'Nubra Valley', 'Pangong')."""
    
    result = get_weather_for_location(location)
    return result


@tool
def get_road_status(route: str) -> str:
    """Get current road status and conditions for Ladakh routes and passes.
    Use this when asking about road conditions, pass status, or route accessibility.
    Input should be the route or pass name (e.g., 'Khardung La', 'Chang La', 'Manali to Leh')."""
    
    data = _load_json("routes.json")
    
    route_lower = route.lower()
    
    for pass_name, info in data["routes"].items():
        if any(keyword in route_lower for keyword in info.get("keywords", [pass_name.lower()])):
            result = f"**{pass_name}**\n"
            result += f"- Elevation: {info['elevation']}\n"
            result += f"- Typical open season: {info['open_season']}\n"
            result += f"- Current status: {info.get('current_status', 'Check locally for latest updates')}\n"
            result += f"- Road condition: {info.get('road_condition', 'Varies by season')}\n"
            result += f"- Tips: {info['tips']}\n"
            return result
    
    return (
        "Road conditions in Ladakh change frequently. Key passes like Khardung La and "
        "Chang La are typically open from June to October. Always check with local taxi "
        "drivers or the BRO (Border Roads Organisation) for the latest updates before "
        "traveling. Carry chains if traveling early/late season."
    )


@tool
def get_altitude_advice(query: str) -> str:
    """Get altitude sickness prevention advice and acclimatization tips for Ladakh.
    Use this when the user asks about altitude sickness, AMS, acclimatization, or health at high altitude."""
    
    return (
        "**Altitude Sickness (AMS) Prevention for Ladakh:**\n\n"
        "**Before arriving:**\n"
        "- Stay hydrated (3-4 liters/day) starting 2 days before\n"
        "- Avoid alcohol 24 hours before and after arrival\n"
        "- Consult your doctor about Diamox (Acetazolamide) — commonly prescribed as a preventive\n"
        "- Get adequate sleep before travel\n\n"
        "**On arrival in Leh (11,500 ft / 3,505m):**\n"
        "- REST for the first 24 hours — no sightseeing on Day 1\n"
        "- Walk slowly, avoid running or heavy exertion\n"
        "- Eat light meals\n"
        "- Keep monitoring for symptoms\n\n"
        "**AMS Symptoms to watch for:**\n"
        "- Headache (most common)\n"
        "- Nausea or vomiting\n"
        "- Dizziness or lightheadedness\n"
        "- Fatigue and loss of appetite\n"
        "- Difficulty sleeping\n\n"
        "**When to descend IMMEDIATELY:**\n"
        "- Severe headache not relieved by paracetamol\n"
        "- Confusion or disorientation\n"
        "- Loss of coordination (ataxia)\n"
        "- Breathlessness at rest\n"
        "- Bluish lips or fingernails\n\n"
        "**Key rule:** If symptoms worsen, DESCEND. Altitude sickness can be fatal if ignored.\n\n"
        "**Emergency contacts in Leh:**\n"
        "- SNM Hospital: 01982-252014\n"
        "- Sonam Norbu Memorial Hospital is the main hospital in Leh"
    )


@tool
def find_homestays(area: str) -> str:
    """Find homestays and local accommodation in a specific Ladakh area.
    Use this when the user asks about where to stay, homestays, or local accommodation.
    Input should be the area name (e.g., 'Nubra Valley', 'Pangong', 'Tso Moriri')."""
    
    data = _load_json("homestays.json")
    
    area_lower = area.lower()
    
    for region, info in data["homestays"].items():
        if any(keyword in area_lower for keyword in info.get("keywords", [region.lower()])):
            result = f"**Homestays in {region}:**\n\n"
            for stay in info.get("options", []):
                result += f"- **{stay['name']}**: {stay.get('description', '')}\n"
                result += f"  Price: {stay.get('price', 'Contact directly')}\n"
                if stay.get("contact"):
                    result += f"  Contact: {stay['contact']}\n"
                result += "\n"
            result += "**Tip:** Book homestays in advance during peak season (June-September). "
            result += "Homestays offer authentic local food and cultural experiences."
            return result
    
    return (
        "Ladakh has wonderful homestay options across all major tourist areas. "
        "Popular homestay regions include Nubra Valley, Pangong Lake area, "
        "Tso Moriri, and villages around Leh like Hemis and Thiksey. "
        "Prices range from ₹800-2500/night including meals. "
        "Book via local travel agents or directly — many don't have online booking."
    )


@tool
def get_cultural_etiquette(topic: str) -> str:
    """Get cultural etiquette and do's/don'ts for visiting Ladakh.
    Use this when asking about monastery visits, local customs, dress code, or cultural tips."""
    
    data = _load_json("cultural_guide.json")
    
    topic_lower = topic.lower()
    
    for category, info in data["guidelines"].items():
        if any(keyword in topic_lower for keyword in info.get("keywords", [category.lower()])):
            result = f"**{category}:**\n\n"
            for tip in info.get("tips", []):
                result += f"• {tip}\n"
            return result
    
    return (
        "**General Cultural Etiquette for Ladakh:**\n\n"
        "**Monasteries:**\n"
        "• Remove shoes before entering prayer halls\n"
        "• Walk clockwise around monasteries and stupas\n"
        "• Don't touch religious artifacts or murals\n"
        "• Ask before photographing monks or ceremonies\n"
        "• Dress modestly — cover shoulders and knees\n\n"
        "**General:**\n"
        "• Don't point feet toward people or religious objects\n"
        "• Accept offerings (tea, food) with both hands\n"
        "• Don't litter — Ladakh's ecosystem is fragile\n"
        "• Respect prayer flags — don't step on or remove them\n"
        "• Learn a few Ladakhi words: 'Julley' (hello/thank you), 'Juk' (sit down)\n"
        "• Don't buy fossils or artifacts — it's illegal\n"
        "• Carry reusable water bottles — plastic waste is a major problem"
    )


def get_tools():
    """Return all available tools for the agent."""
    return [
        check_permit_requirements,
        get_weather_info,
        get_road_status,
        get_altitude_advice,
        find_homestays,
        get_cultural_etiquette,
    ]
