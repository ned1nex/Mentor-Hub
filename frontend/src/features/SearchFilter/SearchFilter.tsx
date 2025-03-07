"use client";
import { useState } from "react";
import styles from "./SearchFilter.module.css";

const predefinedTags = [
  "Frontend", "Backend", "UI/UX", "Data Science", "Product Management",
  "DevOps", "Cybersecurity", "Blockchain", "AI/ML"
];

const SearchFilter = ({ onApplyFilters }: { onApplyFilters: (tags: string[]) => void }) => {
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [customTag, setCustomTag] = useState("");

  const toggleTag = (tag: string) => {
    setSelectedTags(prev =>
      prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]
    );
  };

  const addCustomTag = () => {
    if (customTag.trim() && !selectedTags.includes(customTag)) {
      setSelectedTags(prev => [...prev, customTag.trim()]);
      setCustomTag("");
    }
  };

  return (
    <>
      <button className={styles.filterBtn} onClick={() => setIsFilterOpen(true)}>
        <span>Фильтры</span>
      </button>

      {isFilterOpen && (
        <div className={styles.filterOverlay} onClick={() => setIsFilterOpen(false)}>
          <div className={styles.filterContainer} onClick={e => e.stopPropagation()}>
            <h2>Выберите фильтры</h2>
            <div className={styles.tagContainer}>
              {predefinedTags.map(tag => (
                <span
                  key={tag}
                  className={`${styles.tag} ${selectedTags.includes(tag) ? styles.activeTag : ""}`}
                  onClick={() => toggleTag(tag)}
                >
                  {tag}
                </span>
              ))}
            </div>
            <div className={styles.customTag}>
              <input
                type="text"
                placeholder="Введите свой тег..."
                value={customTag}
                onChange={e => setCustomTag(e.target.value)}
              />
              <button onClick={addCustomTag}>Добавить</button>
            </div>
            <div className={styles.selectedTags}>
              {selectedTags.map(tag => (
                <span key={tag} className={styles.selectedTag}>
                  {tag} <span onClick={() => toggleTag(tag)}>✖</span>
                </span>
              ))}
            </div>
            <button className={styles.applyBtn} onClick={() => { onApplyFilters(selectedTags); setIsFilterOpen(false); }}>
              Применить
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default SearchFilter;
