import { useState } from "react";
import { SendIcon } from "../Icons";

export const Footer = ({config, query, setQuery, sendMessage}) => {
  const [isHovered, setIsHovered] = useState(-1);
  const [isFocused, setIsFocused] = useState(false);
  const changeQuery = (e) => {
    setQuery(e.target.value);
  };
  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage(query);
    }
  };
  const promptStyle = (index, isbutton) => {
    return {
      borderColor: config["primary-color"],
      color: isHovered != index ? config["primary-color"] : "#FFFFFF",
      backgroundColor: isHovered == index ? config["primary-color"] : "#FFFFFF",
    };
  };
  const primaryStyle = {
    color: config["primary-color"],
  };

  const textAreaStyle = {
    borderColor: isFocused ? config["primary-color"] : "#d0d5dd",
  };
  return (
    <div className="sai-footer">
      <div className="sai-chatbox-input-area">
        <div className="quick-prompts">
          {config["quick_prompts"] ? (
            config["quick_prompts"].map((prompt, index) => {
              if (prompt.link) {
                return (
                  <a
                    key={index}
                    target="_blank"
                    className="primary-color"
                    style={promptStyle(index)}
                    onMouseOver={() => setIsHovered(index)}
                    onMouseOut={() => setIsHovered(-1)}
                    href={prompt.link}
                  >
                    {prompt.title}
                  </a>
                );
              } else
                return (
                  <button
                    key={index}
                    className="primary-color"
                    onClick={() => sendMessage(prompt.prompt)}
                    type="button"
                    style={promptStyle(index, true)}
                    onMouseOver={() => setIsHovered(index)}
                    onMouseOut={() => setIsHovered(-1)}
                  >
                    {prompt.title}
                  </button>
                );
            })
          ) : (
            <div />
          )}
        </div>
        <div className="sai-chatbox-input relative flex">
          <textarea
            id="autosize-textarea"
            placeholder={config["input-placeholder"]}
            onChange={changeQuery}
            onKeyDown={handleKeyDown}
            value={query}
            style={textAreaStyle}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
          ></textarea>
          <button
            type="button"
            className="btn absolute sai-send primary-color"
            onClick={() => sendMessage(query)}
            style={primaryStyle}
          >
            <SendIcon />
          </button>
        </div>
      </div>

      {config["hide-powered-by"] == "on" && config["hide-powered-by"] ? (
        <div />
      ) : (
        <div className="sai-chatbox-footer">
          <p>
            Powered by{" "}
            <a
              href="https://wishartgroup.co.uk"
              className="primary-color"
              target="_blank"
              style={{color:"rgb(238, 17, 71)"}}
            >
              wishartgroup
            </a>
          </p>
        </div>
      )}
    </div>
  );
};
