import { Dispatch, FC, SetStateAction } from "react";
import styles from "./SwitchItem.module.css";

interface IProps {
    item: string;
    isActive: boolean;
    setActiveItem: Dispatch<SetStateAction<number>>;
    index: number;
}

const SwitchItem: FC<IProps> = ({ item, isActive, setActiveItem, index }) => {
    return (
        <div
            style={{
                backgroundColor: isActive ? "#121212" : "transparent",
                color: isActive ? "#ffffff" : "#a0a0a0",
            }}
            className={styles.wrapper}
            onClick={() => setActiveItem(index)}>
            {item}
        </div>
    );
};

export default SwitchItem;
