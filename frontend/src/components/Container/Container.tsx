import { HTMLAttributes, ReactNode } from "react";
import styles from "./Container.module.css";

function Container({
    children,
    ...props
}: HTMLAttributes<HTMLDivElement> & { children: ReactNode }) {
    return (
        <div {...props} className={styles.container}>
            {children}
        </div>
    );
}

export default Container;
