import React from "react";
import CharacteristicsFilter from "./CharacteristicsFilter";

export default function CharacteristicsFilterContainer({
    handleSearch,
    toggleDropdown,
    isOpen,
    dropdownRef,
    characteristics,
    handleOptionSelect,
    selectedOptions,
    handleShowAll,
    rotation,
}) {
    return (
        <div className="h-full bg-white rounded-full shadow flex items-center relative">
            <input
                className="h-full px-3 flex-grow border-none outline-none"
                type="text"
                onChange={handleSearch}
                onClick={toggleDropdown}
            />

            {isOpen && (
                <div
                    ref={dropdownRef}
                    className="absolute top-full left-0 w-full bg-white rounded-[10%] shadow-md mt-1 overflow-hidden"
                >
                    <ul className="overflow-y-auto max-h-[200px]">
                        <CharacteristicsFilter
                            characteristics={characteristics}
                            handleOptionSelect={handleOptionSelect}
                            selectedOptions={selectedOptions}
                        />
                    </ul>
                    <div className="w-full px-3 py-2 hover:bg-gray-100 cursor-pointer text-center" onClick={handleShowAll}>
                        Show All Categories
                    </div>
                </div>
            )}

            <button
                className="px-3 transition-transform duration-300"
                style={{ transform: `rotate(${rotation}deg)` }}
                onClick={toggleDropdown}
            >
                ✈️
            </button>
        </div>
    );
}
