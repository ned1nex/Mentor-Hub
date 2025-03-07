import Link, { LinkProps } from "next/link";
import Action from "../../../components/Action/Action";

function NavLink({
    href,
    children,
    asChild = false,
    variant = "default",
}: LinkProps & {
    children?: React.ReactNode | undefined;
    variant?: "default" | "negative" | "emphasized" | undefined;
} & React.RefAttributes<HTMLAnchorElement> & { asChild?: boolean }) {
    return (
        <Link href={href}>
            <Action asChild={asChild} variant={variant}>
                {children}
            </Action>
        </Link>
    );
}

export default NavLink;
