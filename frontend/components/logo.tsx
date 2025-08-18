import { cn } from '../lib/utils'

export const Logo = ({ className }: { className?: string }) => {
    return (
        <svg
            className={cn('h-6 w-auto', className)}
            viewBox="0 0 120 24"
            xmlns="http://www.w3.org/2000/svg"
            role="img"
            aria-label="CodeVision">
            <defs>
                <linearGradient id="cv-grad" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stopColor="#4F46E5" />
                    <stop offset="100%" stopColor="#06B6D4" />
                </linearGradient>
            </defs>
            <g fill="url(#cv-grad)">
                <circle cx="12" cy="12" r="10" opacity="0.15" />
                <path d="M12 5a7 7 0 1 0 7 7h-2a5 5 0 1 1-5-5V5z" />
                <circle cx="12" cy="12" r="2" />
            </g>
            <text x="28" y="16" fontFamily="Inter, system-ui, Arial" fontWeight="700" fontSize="14" fill="#0F172A">Code</text>
            <text x="63" y="16" fontFamily="Inter, system-ui, Arial" fontWeight="700" fontSize="14" fill="#0EA5E9">Vision</text>
        </svg>
    )
}

export const LogoIcon = ({ className }: { className?: string }) => {
    return (
        <svg className={cn('size-8', className)} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="cv-grad-small" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stopColor="#4F46E5" />
                    <stop offset="100%" stopColor="#06B6D4" />
                </linearGradient>
            </defs>
            <circle cx="12" cy="12" r="10" fill="url(#cv-grad-small)" opacity="0.2" />
            <path d="M12 6a6 6 0 1 0 6 6h-2a4 4 0 1 1-4-4V6z" fill="#06B6D4" />
            <circle cx="12" cy="12" r="2" fill="#0EA5E9" />
        </svg>
    )
}

export const LogoStroke = ({ className }: { className?: string }) => {
    return (
        <svg
            className={cn('size-7 w-7', className)}
            viewBox="0 0 71 25"
            fill="none"
            xmlns="http://www.w3.org/2000/svg">
            <path
                d="M61.25 1.625L70.75 1.5625C70.75 4.77083 70.25 7.79167 69.25 10.625C68.2917 13.4583 66.8958 15.9583 65.0625 18.125C63.2708 20.25 61.125 21.9375 58.625 23.1875C56.1667 24.3958 53.4583 25 50.5 25C46.875 25 43.6667 24.2708 40.875 22.8125C38.125 21.3542 35.125 19.2083 31.875 16.375C29.75 14.4167 27.7917 12.8958 26 11.8125C24.2083 10.7292 22.2708 10.1875 20.1875 10.1875C18.0625 10.1875 16.25 10.7083 14.75 11.75C13.25 12.75 12.0833 14.1875 11.25 16.0625C10.4583 17.9375 10.0625 20.1875 10.0625 22.8125L0 22.9375C0 19.6875 0.479167 16.6667 1.4375 13.875C2.4375 11.0833 3.83333 8.64583 5.625 6.5625C7.41667 4.47917 9.54167 2.875 12 1.75C14.5 0.583333 17.2292 0 20.1875 0C23.8542 0 27.1042 0.770833 29.9375 2.3125C32.8125 3.85417 35.7708 5.97917 38.8125 8.6875C41.1042 10.7708 43.1042 12.3333 44.8125 13.375C46.5625 14.375 48.4583 14.875 50.5 14.875C52.6667 14.875 54.5417 14.3125 56.125 13.1875C57.75 12.0625 59 10.5 59.875 8.5C60.7917 6.5 61.25 4.20833 61.25 1.625Z"
                fill="none"
                strokeWidth={0.5}
                stroke="currentColor"
            />
        </svg>
    )
}
