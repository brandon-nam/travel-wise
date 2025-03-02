import axios from "axios";

export async function fetchComments() {
    const results = await axios.get("http://localhost:3203/comments");

    return results.data
}

export async function fetchPosts() {
    const results = await axios.get("http://localhost:3203/posts");

    return results.data
}