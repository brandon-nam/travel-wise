import axios from "axios";

export async function fetchComments() {
    const results = await axios.get("http://localhost:3203/comments");

    // const suggestions = results.data.filter((result) => result.classification === "travel_suggestion");

    return results.data
}

