import { Dispatch, FC, SetStateAction } from "react";
import styles from "./Switch.module.css";
import SwitchItem from "../SwitchItem/SwitchItem";

interface IProps {
    items: string[];
    activeItem: number;
    setActiveItem: Dispatch<SetStateAction<number>>;
}

const Switch: FC<IProps> = ({ items, activeItem, setActiveItem }) => {
    return (
        <div className={styles.wrapper}>
            {items.map((el, index) => (
                <SwitchItem
                    setActiveItem={setActiveItem}
                    index={index}
                    item={el}
                    key={index}
                    isActive={activeItem === index}
                />
            ))}
        </div>
    );
};

export default Switch;
