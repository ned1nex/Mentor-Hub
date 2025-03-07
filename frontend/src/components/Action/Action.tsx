import { clsx } from "clsx";
import styles from "./Action.module.css";

function Action({
    children,
    asChild = false,
    variant = "default",
}: {
    children?: React.ReactNode | undefined;
    variant?: "default" | "negative" | "alt" | "emphasized" | undefined;
} & React.RefAttributes<HTMLAnchorElement> & { asChild?: boolean }) {
    return (
        <span
            className={clsx(
                !asChild && [
                    styles.action,
                    variant == "negative" && styles.negative,
                    variant == "alt" && styles.alt,
                    variant == "emphasized" && styles.emphasized,
                ],
            )}>
            {children}
        </span>
    );
}

export default Action;
