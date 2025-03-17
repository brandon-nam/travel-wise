export const sortSuggestions = (suggestions, sortOrder) => {
    return [...suggestions].sort((a, b) => {
        return sortOrder === "ascending" ? a.score - b.score : b.score - a.score;
    });
};