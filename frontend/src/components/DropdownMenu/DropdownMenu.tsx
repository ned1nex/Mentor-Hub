import NavLink from "@/src/widgets/Header/NavLink/NavLink";
import { Menu, MenuButton, MenuItem, MenuItems, Transition } from "@headlessui/react";
import { clsx } from "clsx";
import { Fragment, ReactNode } from "react";
import styles from "./DropdownMenu.module.css";

export interface DropdownMenuItem {
    label: string;
    onClick?: () => void;
    href?: string;
}

interface DropdownMenuProps {
    trigger: ReactNode;
    items: DropdownMenuItem[];
    links?: boolean;
}

function DropdownMenu({ trigger, items, links = false }: DropdownMenuProps) {
    return (
        <Menu as="div" className={styles.menu}>
            <div>
                <MenuButton>{trigger}</MenuButton>
            </div>
            <Transition
                as={Fragment}
                enter={styles.enter}
                enterFrom={styles.enterFrom}
                enterTo={styles.enterTo}
                leave={styles.leave}
                leaveFrom={styles.leaveFrom}
                leaveTo={styles.leaveTo}>
                <MenuItems className={styles.menuItems}>
                    {items.map((item, index) => (
                        <MenuItem key={index}>
                            {({ focus }) =>
                                links ? (
                                    <NavLink href={item.href || "/"} asChild>
                                        <div
                                            className={clsx(
                                                styles.menuItem,
                                                focus && styles.active,
                                            )}
                                            onClick={item.onClick}>
                                            {item.label}
                                        </div>
                                    </NavLink>
                                ) : (
                                    <div
                                        className={clsx(styles.menuItem, focus && styles.active)}
                                        onClick={item.onClick}>
                                        {item.label}
                                    </div>
                                )
                            }
                        </MenuItem>
                    ))}
                </MenuItems>
            </Transition>
        </Menu>
    );
}

export default DropdownMenu;
