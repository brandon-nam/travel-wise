import { useQuery } from "@tanstack/react-query";
import { fetchSuggestionsByCountry } from "../lib/API";

const filterAndFlattenLocations = (data) => {
    const locations = {};
    const result = [];
    let appendIndex = 0;

    data.forEach((suggestion) => {
        try {
            const { location_coordinates, ...rest } = suggestion;
            location_coordinates.forEach((location) => {
                const locationKey = `${location.lat},${location.lng}`;
                if (!locations[locationKey]) {
                    locations[locationKey] = appendIndex;
                    result[appendIndex] = {
                        location_name: location.location_name,
                        characteristic: location.characteristic,
                        lat: location.lat,
                        lng: location.lng,
                        score: rest.score,
                        comments: [rest],
                    };
                    appendIndex++;
                } else {
                    const index = locations[locationKey];
                    result[index].comments.push(rest);
                    result[index].score += rest.score;
                }
            });
        } catch (e) {
            console.log("error: ", e);
        }
    });
    return result;
};

export const useSuggestions = (country) => {
    return useQuery({
        queryKey: ["travelSuggestions", country],
        queryFn: () => fetchSuggestionsByCountry(country),
        select: (data) => filterAndFlattenLocations(data),
        staleTime: Infinity,
    });
};