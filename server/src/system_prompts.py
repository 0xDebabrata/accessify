from .prompt_details import PromptDetails
from .enum_types import ElementType


prompts = {
    ElementType.BUTTON: PromptDetails(
        sysMessage="make the elements more accessible, return code only, add all necessary attributes",
        userMessage="Make the following buttons responsive with the given examples\n\n\n",
        temperature=0.5,
    ),
    ElementType.ANCHOR: PromptDetails(
        sysMessage="You are a pro at making the web accessible.You can look at urls and provide corresponding aria-labels for making the page more accessible",
        userMessage="""
            Example:
            Given URLs:
            http://www.w3.org/WAI/sitemap.html
            http://www.w3.org/WAI/search.php

            Response:
            WAI sitemap for web accessibility information
            WAI search for web accessibility information

            Here are some URLs. Please suggest 1 line aria-labels for each of the URLs in a new line. 
            Give your response in a new line and don't provide anything else.
        """,
        temperature=0.5,
    ),
}
