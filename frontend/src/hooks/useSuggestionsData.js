import { useQuery } from "@tanstack/react-query";
import { fetchSuggestionsByCountry } from "../lib/API";

export const useSuggestionsData = (country) => {
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
                            score: rest.score, // score of the first comment
                            // but we'll need to decide if we want to keep every post url or the one with the highest karma
                            comments: [rest],
                        };
                        appendIndex++;
                    } else {
                        // if two comments talk about the same location, append comment
                        const index = locations[locationKey];
                        let { comments, score, ..._ } = result[index];
                        // combine the karma scores
                        score += rest.score;
                        comments = [...comments, rest]; // appending rest
                        result[index]["comments"] = comments;
                        result[index]["score"] = score;
                    }
                });
            } catch (e) {
                console.log("error: ", e);
            }
        });

        console.log(result);
        return result;

    };

    const suggestionQuery = useQuery({
        queryKey: ["travelSuggestions", country],
        queryFn: () => fetchSuggestionsByCountry(country),
        select: (data) => filterAndFlattenLocations(data),
        staleTime: Infinity,
    });

    const suggestionData = suggestionQuery.data;
    

    return { suggestionData:  }
}

