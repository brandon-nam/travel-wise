import { useQuery } from "@tanstack/react-query";
import { fetchCharacteristics } from "../lib/API";

export const useLocationCharacteristics = () => {
    return useQuery({
        queryKey: ["suggestionsCharacteristics"],
        queryFn: () => fetchCharacteristics("travel-suggestion"),
        staleTime: Infinity,
    });
};