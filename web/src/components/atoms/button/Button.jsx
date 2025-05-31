import styles from "./Button.module.css"
import { Link } from "react-router-dom";


export const Button = ({
    primary,
    secondary,
    accent,
    dark,
    className,
    children,
    navigateTo,
    ...props
}) => {
    const baseClasses = 'btn ' + styles.appBtn;


    const colorClass = primary
        ? 'bg-primario text-light'
        : secondary
            ? 'bg-secundario'
            : dark
                ? 'bg-dark text-light'
                : accent
                    ? 'bg-accent text-light'
                    : '';


    const allClasses = [baseClasses, colorClass, className].filter(Boolean).join(' ');


    if (navigateTo) {
        return (
            <Link to={navigateTo} className={allClasses} {...props}>
                {children}
            </Link>
        )
    }

    return (
        <button className={allClasses} {...props}>
            {children}
        </button>
    )

};