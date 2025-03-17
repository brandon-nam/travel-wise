export const sortComments = (comments, sortOrder) => {
    return [...comments].sort((a, b) => {
        return sortOrder === "ascending" ? a.score - b.score : b.score - a.score;
    });
};