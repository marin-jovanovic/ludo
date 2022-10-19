import countryNameJson from "/public/assets/layers/country_names.json";
import axios from 'axios';

async function getLocations() {
    let r = await axios.get(countryNameJson);
    r = r.data;
    return Object.keys(r);
}

export const jsonManager = {
    getLocations
}

