import React, { useState, createContext } from 'react';

const QueryParametersContext = createContext();

export function QueryParametersProvider({ children }) {
    const defaultSuggestionLink = "/suggestions?";
    const defaultTipLink = "/tips?";
    const [suggestionLink, setSuggestionLink] = useState(defaultSuggestionLink);
    const [tipLink, setTipLink] = useState(defaultTipLink);

    function updateLinks(country) {
        setSuggestionLink(defaultSuggestionLink + "country=" + country); 
        setTipLink(defaultTipLink + "country=" + country); 
    }

    return (
        <QueryParametersContext.Provider value={{ suggestionLink, tipLink, updateLinks }}>
            {children}
        </QueryParametersContext.Provider>
    );
}

export default QueryParametersContext;