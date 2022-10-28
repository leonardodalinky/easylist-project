"""
A simple parser for easylist filter format.

Refer to github project [adblockparser](https://github.com/scrapinghub/adblockparser).
"""
import re
from os import PathLike
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Union

from attrs import define, field

BINARY_OPTIONS = [
    "script",
    "image",
    "stylesheet",
    "object",
    "xmlhttprequest",
    "object-subrequest",
    "subdocument",
    "document",
    "elemhide",
    "other",
    "background",
    "xbl",
    "ping",
    "dtd",
    "media",
    "third-party",
    "match-case",
    "collapse",
    "donottrack",
    "websocket",
]
OPTIONS_SPLIT_PAT = ",(?=~?(?:%s))" % ("|".join(BINARY_OPTIONS + ["domain"]))
OPTIONS_SPLIT_RE = re.compile(OPTIONS_SPLIT_PAT)


@define(kw_only=True)
class Rule:
    raw_rule_text: str
    domain: str
    is_exception: bool = False
    is_html_rule: bool = False
    options: Dict[str, Any] = field(factory=dict)

    @classmethod
    def parse(cls, rule_text: str) -> List["Rule"]:
        args = dict()
        rule_text = rule_text.strip()
        args["raw_rule_text"] = rule_text
        is_comment = not rule_text or rule_text.startswith(("!", "[Adblock"))
        if is_comment:
            return list()
        args["is_html_rule"] = "##" in rule_text or "#@#" in rule_text

        if not args["is_html_rule"]:
            args["is_exception"] = rule_text.startswith("@@")
            if args["is_exception"]:
                # strip rule string for domain parsing
                rule_text = rule_text[2:]

            if "$" in rule_text:
                rule_text, opts_text = rule_text.split("$", 1)
                raw_opts = cls._split_options(opts_text)
                args["options"] = dict(cls._parse_option(opt) for opt in raw_opts)

            if rule_text.startswith("||"):
                rule_text = rule_text[2:]
                d1 = rule_text.split("^", 1)[0]
                d2 = rule_text.split("/", 1)[0]
                args["domain"] = d1 if len(d1) < len(d2) else d2
                return [cls(**args)]
            else:
                # ignore other form
                return list()
        else:
            sep = "##" if "##" in rule_text else "#@#"
            domains_text = rule_text.split(sep, 1)[0]
            domains = domains_text.split(",")

            ret = list()
            for domain in domains:
                new_args = dict(args)
                if domain.startswith("~"):
                    new_args["domain"] = domain[1:]
                else:
                    new_args["domain"] = domain
                if "domain" in new_args:
                    ret.append(cls(**new_args))
            return ret

    @classmethod
    def _split_options(cls, options_text):
        return OPTIONS_SPLIT_RE.split(options_text)

    @classmethod
    def _parse_domain_option(cls, text):
        domains = text[len("domain=") :]
        parts = domains.replace(",", "|").split("|")
        return dict(cls._parse_option_negation(p) for p in parts)

    @classmethod
    def _parse_option_negation(cls, text):
        return text.lstrip("~"), not text.startswith("~")

    @classmethod
    def _parse_option(cls, text):
        if text.startswith("domain="):
            return "domain", cls._parse_domain_option(text)
        return cls._parse_option_negation(text)


@define(kw_only=True)
class Rules:
    rules: List[Rule]
    time: datetime

    def __getitem__(self, index):
        assert isinstance(index, int), f"Index must be integer, but got {index}"
        return self.rules[index]

    @classmethod
    def from_file(cls, filter_path: Union[str, PathLike], time: datetime):
        filter_path = Path(filter_path)
        assert filter_path.exists() and filter_path.is_file(), f"Filter file not found: {filter_path}"
        assert time is not None
        with filter_path.open("r", encoding="utf-8") as fp:
            lines = fp.readlines()
            rules = list(rule for line in lines for rule in Rule.parse(line))
        return cls(rules=rules, time=time)