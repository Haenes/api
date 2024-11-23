import { useRouteError } from "react-router";

export function ErrorPage() {
    const error = useRouteError();

    return (
        <div
            id="error-page"
            className="h-screen w-screen items-center justify-center flex flex-row"
        >
            <h1 className="text-center">
                <i className="font-medium">{error.status}</i>
                <i className="font-thin text-5xl px-2"> | </i>
                <i className="font-normal">{error.statusText}</i>
            </h1>
        </div>
    );
}
