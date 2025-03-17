import axios from "axios";

export async function fetchComments() {
    const results = await axios.get("http://localhost:3203/comments");

    return results.data
}

export async function fetchSuggestions() {
    const results = await axios.get("http://localhost:3203/comments?classification=travel-suggestion");

    return results.data
}

export async function fetchTips() {
    const results = await axios.get("http://localhost:3203/comments?classification=travel-tip");

    return results.data
}

export async function fetchSuggestionsByCountry(country) {
    const results = await axios.get(`http://localhost:3203/comments?classification=travel-suggestion&country=${country}`);
    
    return results.data
}

export async function fetchTipsByCountry(country) {
    const results = await axios.get(`http://localhost:3203/comments?classification=travel-suggestion&country=${country}`);

    return results.data
}


export async function fetchPosts() {
    const results = await axios.get("http://localhost:3203/posts");

    return results.data
}

export async function fetchCharacteristics(classification) {
    const results = await axios.get(`http://localhost:3203/characteristics-locations`); 

    return results.data
}