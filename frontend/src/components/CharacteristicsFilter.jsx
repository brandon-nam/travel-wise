export default function CharacteristicsFilter({ characteristics, handleOptionSelect, selectedOptions }) {
    return (
        <>
            {characteristics.map((option) => (
                <div onClick={() => handleOptionSelect(option)}>
                    <li key={option} className="px-3 py-2 hover:bg-gray-100 cursor-pointer flex items-center">
                        <input
                            type="checkbox"
                            id={option}
                            checked={selectedOptions.includes(option)}
                            onChange={() => {}}
                            className="mr-2"
                        />
                        <div className="cursor-pointer">{option}</div>
                    </li>
                </div>
            ))}
        </>
    );
}
