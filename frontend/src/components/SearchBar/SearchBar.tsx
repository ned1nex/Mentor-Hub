import styles from './SearchBar.module.css';
import { useState } from 'react';

interface SearchBarProps {
    onSearch: (query: string) => void;
}

const SearchBar = ({ onSearch }: SearchBarProps) => {
    const [query, setQuery] = useState('');

    const handleSearch = () => {
        onSearch(query);
    };

    return (
        <div className={styles.searchBar}>
            <input
                type="text"
                placeholder="Введите запрос..."
                className={styles.input}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />
            <button className={styles.searchBtn} onClick={handleSearch}>Поиск</button>
        </div>
    );
};

export default SearchBar;
