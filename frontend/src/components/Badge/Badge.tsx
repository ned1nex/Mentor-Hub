import clsx from "clsx";
import styles from "./Badge.module.css";

function Badge({
    children,
    variant = "default",
}: {
    children?: React.ReactNode | undefined;
    variant?: "default" | "negative" | "alt" | undefined;
}) {
    return <span className={clsx(styles.badge, variant == "alt" && styles.alt)}>{children}</span>;
}

export default Badge;
