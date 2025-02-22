## API Gateway Validation Test Results



## ====== Testing qrag-llm  2025-02-16_044010 ======


## ====== clean_requests for qrag-llm ======

## clean_requests           Request 1: Complete matching Portal API Gateway test
Original: {
  "description": "Complete matching Portal API Gateway test",
  "request": {
    "metadata": {
      "timestamp": "2024-06-13T11:46:33.651753",
      "user_id": "default",
      "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
      "bot_version": "2.0",
      "routes_info": {
        "routes_flow_name": "3 routes, separate route prompts",
        "upper_sim_bound": 0.9,
        "lower_sim_bound": 0.3,
        "max_sim": "0.216",
        "max_stars": 5,
        "routes_dict_content": {
          "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
        }
      }
    },
    "content": {
      "user_question": "What should I eat for lunch?",
      "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
      "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
      "quoted_qa": "",
      "ai_answer": "WAITING FOR LLM RESPONSE",
      "chunks": {
        "max_sim": "0.216",
        "max_stars": 5,
        "chunks": []
      }
    }
  }
}
Complete: {
  "description": "Complete matching Portal API Gateway test",
  "request": {
    "metadata": {
      "timestamp": "2024-06-13T11:46:33.651753",
      "user_id": "default",
      "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
      "bot_version": "2.0",
      "routes_info": {
        "routes_flow_name": "3 routes, separate route prompts",
        "upper_sim_bound": 0.9,
        "lower_sim_bound": 0.3,
        "max_sim": "0.216",
        "max_stars": 5,
        "routes_dict_content": {
          "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
        }
      }
    },
    "content": {
      "user_question": "What should I eat for lunch?",
      "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
      "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
      "quoted_qa": "",
      "ai_answer": "WAITING FOR LLM RESPONSE",
      "chunks": {
        "max_sim": "0.216",
        "max_stars": 5,
        "chunks": []
      }
    }
  }
}

### DIRECT LAMBDA INVOCATION
Lambda response payload: {
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 200,
  "body": "{\"status\": \"Success\", \"response\": {\"metadata\": {\"timestamp\": \"2024-06-13T11:46:33.651753\", \"user_id\": \"default\", \"vector_index_name\": \"deutsch-transcript-qrag-83f-20250202\", \"bot_version\": \"2.0\", \"routes_info\": {\"routes_flow_name\": \"3 routes, separate route prompts\", \"upper_sim_bound\": 0.9, \"lower_sim_bound\": 0.3, \"max_sim\": \"0.216\", \"max_stars\": 5, \"routes_dict_content\": {\"routes_dict_name\": \"ROUTES_DICT_DEUTSCH_M1\"}}, \"llm_model\": \"o3-mini\"}, \"content\": {\"user_question\": \"What should I eat for lunch?\", \"route_preamble\": \"Your question is not addressed in David Deutsch's interviews.\", \"prompt_initial\": \"Given your knowledge of David Deutsch and his philosophy...\", \"quoted_qa\": \"\", \"ai_answer\": \"David Deutsch\\u2019s approach to understanding the world is all about seeking good explanations and appreciating the power of ideas\\u2014which means that even a seemingly mundane question like \\u201cWhat should I eat for lunch?\\u201d can be considered in a thoughtful, exploratory way.\\n\\nFrom a Deutsch-inspired perspective you might ask yourself:\\n\\u2022 What are the \\u201cgood explanations\\u201d for why certain foods fuel creativity and robust thinking?  \\n\\u2022 How can you use your meal as a small experiment\\u2014a chance to challenge the status quo of your daily routine and try something new while nourishing both body and mind?\\n\\nSo rather than simply picking what\\u2019s convenient, consider lunch as an opportunity to blend nourishment with innovation. For example:\\n\\u2022 A balanced meal that combines lean proteins, whole grains, and plenty of vegetables might be seen as analogous to a robust theory: each ingredient plays its part and contributes essential \\u201cexplanatory power\\u201d to your overall health.  \\n\\u2022 Alternatively, if you\\u2019re feeling adventurous, why not experiment with a cuisine you\\u2019ve never tried before? In the spirit of seeking new ideas (and as Deutsch would appreciate, a good explanation with surprising insights), a dish with unfamiliar spices or unconventional combinations might inspire a fresh perspective and expand your culinary horizons.\\n\\nUltimately, Deutsch would advocate for an approach that isn\\u2019t dogmatic or based solely on tradition. Instead, let your choice reflect your commitment to seeking out better explanations of how to live well\\u2014even in something as everyday as lunch.\\n\\nSo, what should you eat? Consider crafting a meal that\\u2019s both healthy and innovative\\u2014a creative salad with a mix of greens, perhaps some quinoa or whole grains, a lean protein (like grilled chicken, tofu, or legumes), and a surprising twist in the form of an interesting dressing or a sprinkle of nuts. This way, you nourish yourself while also embracing the spirit of inquiry and creativity that lies at the heart of Deutsch\\u2019s philosophy.\\n\\nBon app\\u00e9tit and may your lunch spark new ideas!\", \"chunks\": {\"max_sim\": \"0.216\", \"max_stars\": 5, \"chunks\": []}, \"cost_pennies_mycalc\": 0.516}}}"
}
Result:
{
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 200,
  "body": "{\"status\": \"Success\", \"response\": {\"metadata\": {\"timestamp\": \"2024-06-13T11:46:33.651753\", \"user_id\": \"default\", \"vector_index_name\": \"deutsch-transcript-qrag-83f-20250202\", \"bot_version\": \"2.0\", \"routes_info\": {\"routes_flow_name\": \"3 routes, separate route prompts\", \"upper_sim_bound\": 0.9, \"lower_sim_bound\": 0.3, \"max_sim\": \"0.216\", \"max_stars\": 5, \"routes_dict_content\": {\"routes_dict_name\": \"ROUTES_DICT_DEUTSCH_M1\"}}, \"llm_model\": \"o3-mini\"}, \"content\": {\"user_question\": \"What should I eat for lunch?\", \"route_preamble\": \"Your question is not addressed in David Deutsch's interviews.\", \"prompt_initial\": \"Given your knowledge of David Deutsch and his philosophy...\", \"quoted_qa\": \"\", \"ai_answer\": \"David Deutsch\\u2019s approach to understanding the world is all about seeking good explanations and appreciating the power of ideas\\u2014which means that even a seemingly mundane question like \\u201cWhat should I eat for lunch?\\u201d can be considered in a thoughtful, exploratory way.\\n\\nFrom a Deutsch-inspired perspective you might ask yourself:\\n\\u2022 What are the \\u201cgood explanations\\u201d for why certain foods fuel creativity and robust thinking?  \\n\\u2022 How can you use your meal as a small experiment\\u2014a chance to challenge the status quo of your daily routine and try something new while nourishing both body and mind?\\n\\nSo rather than simply picking what\\u2019s convenient, consider lunch as an opportunity to blend nourishment with innovation. For example:\\n\\u2022 A balanced meal that combines lean proteins, whole grains, and plenty of vegetables might be seen as analogous to a robust theory: each ingredient plays its part and contributes essential \\u201cexplanatory power\\u201d to your overall health.  \\n\\u2022 Alternatively, if you\\u2019re feeling adventurous, why not experiment with a cuisine you\\u2019ve never tried before? In the spirit of seeking new ideas (and as Deutsch would appreciate, a good explanation with surprising insights), a dish with unfamiliar spices or unconventional combinations might inspire a fresh perspective and expand your culinary horizons.\\n\\nUltimately, Deutsch would advocate for an approach that isn\\u2019t dogmatic or based solely on tradition. Instead, let your choice reflect your commitment to seeking out better explanations of how to live well\\u2014even in something as everyday as lunch.\\n\\nSo, what should you eat? Consider crafting a meal that\\u2019s both healthy and innovative\\u2014a creative salad with a mix of greens, perhaps some quinoa or whole grains, a lean protein (like grilled chicken, tofu, or legumes), and a surprising twist in the form of an interesting dressing or a sprinkle of nuts. This way, you nourish yourself while also embracing the spirit of inquiry and creativity that lies at the heart of Deutsch\\u2019s philosophy.\\n\\nBon app\\u00e9tit and may your lunch spark new ideas!\", \"chunks\": {\"max_sim\": \"0.216\", \"max_stars\": 5, \"chunks\": []}, \"cost_pennies_mycalc\": 0.516}}}"
}

### API GATEWAY INVOCATION
Request being sent to API Gateway:
{
  "metadata": {
    "timestamp": "2024-06-13T11:46:33.651753",
    "user_id": "default",
    "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
    "bot_version": "2.0",
    "routes_info": {
      "routes_flow_name": "3 routes, separate route prompts",
      "upper_sim_bound": 0.9,
      "lower_sim_bound": 0.3,
      "max_sim": "0.216",
      "max_stars": 5,
      "routes_dict_content": {
        "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
      }
    }
  },
  "content": {
    "user_question": "What should I eat for lunch?",
    "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
    "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
    "quoted_qa": "",
    "ai_answer": "WAITING FOR LLM RESPONSE",
    "chunks": {
      "max_sim": "0.216",
      "max_stars": 5,
      "chunks": []
    }
  }
}
Result:
{
  "status": "Success",
  "response": {
    "metadata": {
      "timestamp": "2024-06-13T11:46:33.651753",
      "user_id": "default",
      "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
      "bot_version": "2.0",
      "routes_info": {
        "routes_flow_name": "3 routes, separate route prompts",
        "upper_sim_bound": 0.9,
        "lower_sim_bound": 0.3,
        "max_sim": "0.216",
        "max_stars": 5,
        "routes_dict_content": {
          "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
        }
      },
      "llm_model": "o3-mini"
    },
    "content": {
      "user_question": "What should I eat for lunch?",
      "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
      "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
      "quoted_qa": "",
      "ai_answer": "Drawing on David Deutsch\u2019s approach to knowledge and problem-solving, you might view even a decision as seemingly mundane as \u201cwhat to eat for lunch\u201d as an opportunity to experiment, learn, and refine your understanding. Deutsch stresses that progress comes from taking risks in our ideas and testing them rigorously\u2014so why not apply that to your meal planning, too? Here are a few thoughts inspired by his philosophy:\n\n1.\u2002Treat lunch as an experiment in creativity and nourishment. Rather than defaulting to the usual options, consider a balanced meal that challenges your palate. For example, you could assemble a fresh salad featuring a mix of textures and flavors\u2014a base of leafy greens paired with an array of colorful vegetables, a carefully chosen protein (like grilled chicken, tofu, or legumes), and a drizzle of an innovative dressing you haven\u2019t tried before.\n\n2.\u2002Embrace the idea of \u201coptimism about the future\u201d by choosing food that not only satisfies your hunger today but also fuels your curiosity and productivity tomorrow. Just as Deutsch advocates for seeking better explanations of the world, aim for a meal that elevates both your physical well\u2010being and mental clarity. Whole grains, lean proteins, and healthy fats can help keep your mind sharp so you\u2019re ready to tackle new problems with enthusiasm.\n\n3.\u2002See this decision as a microcosm of the creative process: assemble different ingredients (or ideas) together to see what emerges. Maybe experiment with a fusion dish that blends culinary traditions\u2014a bit like combining diverse theories to gain a more comprehensive understanding of reality. This approach mirrors Deutsch\u2019s view that progress comes from boldly mixing ideas and then letting the best survive criticism.\n\n4.\u2002Finally, if you\u2019re inclined to be methodical like Deutsch, consider gathering data about what works best for you. Over time, keep a mental (or literal) record of meals that give you the energy and clarity to engage with complex problems. Treat your lunch as another domain in which you\u2019re testing hypotheses on how best to live.\n\nIn summary, while I can\u2019t tell you unequivocally \u201cwhat to eat for lunch\u201d without knowing your dietary needs or preferences, you might take a page out of David Deutsch\u2019s book by approaching the choice with curiosity, experimentation, and a commitment to learning. Whether you decide on a vibrant salad with a creative twist, a hearty bowl of soup, or even a daring new fusion dish, let your choice be a reflection of your willingness to test new ideas and refine your \u201ctheory\u201d of what makes a satisfying and nourishing lunch. Enjoy the process\u2014and your meal!",
      "chunks": {
        "max_sim": "0.216",
        "max_stars": 5,
        "chunks": []
      },
      "cost_pennies_mycalc": 0.603
    }
  }
}

## clean_requests           Request 2: Complete matching Portal API Gateway test with large context filename
Original: {
  "description": "Complete matching Portal API Gateway test with large context filename",
  "request": {
    "metadata": {
      "large_context_filename": "deutsch_large_context_v1.md"
    }
  }
}
Complete: {
  "description": "Complete matching Portal API Gateway test with large context filename",
  "request": {
    "metadata": {
      "timestamp": "2024-06-13T11:46:33.651753",
      "user_id": "default",
      "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
      "bot_version": "2.0",
      "routes_info": {
        "routes_flow_name": "3 routes, separate route prompts",
        "upper_sim_bound": 0.9,
        "lower_sim_bound": 0.3,
        "max_sim": "0.216",
        "max_stars": 5,
        "routes_dict_content": {
          "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
        }
      },
      "large_context_filename": "deutsch_large_context_v1.md"
    },
    "content": {
      "user_question": "What should I eat for lunch?",
      "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
      "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
      "quoted_qa": "",
      "ai_answer": "WAITING FOR LLM RESPONSE",
      "chunks": {
        "max_sim": "0.216",
        "max_stars": 5,
        "chunks": []
      }
    }
  }
}

### DIRECT LAMBDA INVOCATION
Lambda response payload: {
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 200,
  "body": "{\"status\": \"Success\", \"response\": {\"metadata\": {\"timestamp\": \"2024-06-13T11:46:33.651753\", \"user_id\": \"default\", \"vector_index_name\": \"deutsch-transcript-qrag-83f-20250202\", \"bot_version\": \"2.0\", \"routes_info\": {\"routes_flow_name\": \"3 routes, separate route prompts\", \"upper_sim_bound\": 0.9, \"lower_sim_bound\": 0.3, \"max_sim\": \"0.216\", \"max_stars\": 5, \"routes_dict_content\": {\"routes_dict_name\": \"ROUTES_DICT_DEUTSCH_M1\"}}, \"large_context_filename\": \"deutsch_large_context_v1.md\", \"llm_model\": \"o3-mini\"}, \"content\": {\"user_question\": \"What should I eat for lunch?\", \"route_preamble\": \"Your question is not addressed in David Deutsch's interviews.\", \"prompt_initial\": \"Given your knowledge of David Deutsch and his philosophy...\", \"quoted_qa\": \"\", \"ai_answer\": \"Drawing on a Deutsch-like approach to solving problems, you might view your lunch not as a trivial decision but as an opportunity to experiment, learn, and improve your state of well-being\\u2014just as we improve our theories by creatively correcting errors and seeking better explanations.\\n\\nConsider your lunch as fuel for creative thought and progress. Instead of defaulting to a habitual meal, why not try something balanced that offers both nourishment and a hint of novelty? For example, you might experiment with a Mediterranean quinoa salad: a composition of fresh greens, protein (such as grilled chicken or tofu), colorful vegetables, a sprinkle of nuts or seeds for both texture and healthy fats, and a drizzle of olive oil and lemon for flavor.\\n\\nThis choice embodies several Deutschian ideas:\\n1. Creativity: Trying a new recipe or mixing ingredients encourages you to break out of rote habits\\u2014mirroring how innovative ideas emerge from challenging standard assumptions.\\n2. Error-Correction: Just as scientific theories are improved by testing and refining, you can adjust the proportions or ingredients next time if you feel something is \\u201coff.\\u201d\\n3. Progress: Fuelling your body with a meal that is both nourishing and engaging can help optimize both physical and mental energy, supporting the kind of creative thinking that drives meaningful progress.\\n\\nUltimately, the best lunch is one that aligns with your nutritional needs, tastes, and desire to be open to new ideas\\u2014much like how good explanations in science are hard to vary once they are fully understood and refined.\\n\\nSo, if you\\u2019re open to a little culinary exploration, why not give a creative, nutrient-rich Mediterranean quinoa salad a try today? Enjoy the process of experimenting with flavors as much as the meal itself, and let that spirit of inquiry carry over into the rest of your day.\", \"chunks\": {\"max_sim\": \"0.216\", \"max_stars\": 5, \"chunks\": []}, \"large_context_filename\": \"deutsch_large_context_v1.md\", \"cost_pennies_mycalc\": 1.823}}}"
}
Result:
{
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 200,
  "body": "{\"status\": \"Success\", \"response\": {\"metadata\": {\"timestamp\": \"2024-06-13T11:46:33.651753\", \"user_id\": \"default\", \"vector_index_name\": \"deutsch-transcript-qrag-83f-20250202\", \"bot_version\": \"2.0\", \"routes_info\": {\"routes_flow_name\": \"3 routes, separate route prompts\", \"upper_sim_bound\": 0.9, \"lower_sim_bound\": 0.3, \"max_sim\": \"0.216\", \"max_stars\": 5, \"routes_dict_content\": {\"routes_dict_name\": \"ROUTES_DICT_DEUTSCH_M1\"}}, \"large_context_filename\": \"deutsch_large_context_v1.md\", \"llm_model\": \"o3-mini\"}, \"content\": {\"user_question\": \"What should I eat for lunch?\", \"route_preamble\": \"Your question is not addressed in David Deutsch's interviews.\", \"prompt_initial\": \"Given your knowledge of David Deutsch and his philosophy...\", \"quoted_qa\": \"\", \"ai_answer\": \"Drawing on a Deutsch-like approach to solving problems, you might view your lunch not as a trivial decision but as an opportunity to experiment, learn, and improve your state of well-being\\u2014just as we improve our theories by creatively correcting errors and seeking better explanations.\\n\\nConsider your lunch as fuel for creative thought and progress. Instead of defaulting to a habitual meal, why not try something balanced that offers both nourishment and a hint of novelty? For example, you might experiment with a Mediterranean quinoa salad: a composition of fresh greens, protein (such as grilled chicken or tofu), colorful vegetables, a sprinkle of nuts or seeds for both texture and healthy fats, and a drizzle of olive oil and lemon for flavor.\\n\\nThis choice embodies several Deutschian ideas:\\n1. Creativity: Trying a new recipe or mixing ingredients encourages you to break out of rote habits\\u2014mirroring how innovative ideas emerge from challenging standard assumptions.\\n2. Error-Correction: Just as scientific theories are improved by testing and refining, you can adjust the proportions or ingredients next time if you feel something is \\u201coff.\\u201d\\n3. Progress: Fuelling your body with a meal that is both nourishing and engaging can help optimize both physical and mental energy, supporting the kind of creative thinking that drives meaningful progress.\\n\\nUltimately, the best lunch is one that aligns with your nutritional needs, tastes, and desire to be open to new ideas\\u2014much like how good explanations in science are hard to vary once they are fully understood and refined.\\n\\nSo, if you\\u2019re open to a little culinary exploration, why not give a creative, nutrient-rich Mediterranean quinoa salad a try today? Enjoy the process of experimenting with flavors as much as the meal itself, and let that spirit of inquiry carry over into the rest of your day.\", \"chunks\": {\"max_sim\": \"0.216\", \"max_stars\": 5, \"chunks\": []}, \"large_context_filename\": \"deutsch_large_context_v1.md\", \"cost_pennies_mycalc\": 1.823}}}"
}

### API GATEWAY INVOCATION
Request being sent to API Gateway:
{
  "metadata": {
    "timestamp": "2024-06-13T11:46:33.651753",
    "user_id": "default",
    "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
    "bot_version": "2.0",
    "routes_info": {
      "routes_flow_name": "3 routes, separate route prompts",
      "upper_sim_bound": 0.9,
      "lower_sim_bound": 0.3,
      "max_sim": "0.216",
      "max_stars": 5,
      "routes_dict_content": {
        "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
      }
    },
    "large_context_filename": "deutsch_large_context_v1.md"
  },
  "content": {
    "user_question": "What should I eat for lunch?",
    "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
    "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
    "quoted_qa": "",
    "ai_answer": "WAITING FOR LLM RESPONSE",
    "chunks": {
      "max_sim": "0.216",
      "max_stars": 5,
      "chunks": []
    }
  }
}
Result:
{
  "status": "Success",
  "response": {
    "metadata": {
      "timestamp": "2024-06-13T11:46:33.651753",
      "user_id": "default",
      "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
      "bot_version": "2.0",
      "routes_info": {
        "routes_flow_name": "3 routes, separate route prompts",
        "upper_sim_bound": 0.9,
        "lower_sim_bound": 0.3,
        "max_sim": "0.216",
        "max_stars": 5,
        "routes_dict_content": {
          "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
        }
      },
      "large_context_filename": "deutsch_large_context_v1.md",
      "llm_model": "o3-mini"
    },
    "content": {
      "user_question": "What should I eat for lunch?",
      "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
      "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
      "quoted_qa": "",
      "ai_answer": "Drawing on David Deutsch\u2019s philosophy\u2014where creativity, the pursuit of good explanations, and the willingness to challenge conventional boundaries are central\u2014you might approach your lunch decision as an experiment in nourishing both body and mind.\n\nConsider this: rather than automatically selecting the familiar, use your lunchtime as an opportunity to try something that isn\u2019t only healthy but also invites new ideas, perhaps even blending elements from different culinary traditions. For example, you could prepare a thoughtfully composed meal that is both nutritionally balanced and creatively satisfying. A mixed salad featuring a variety of textures and flavors (imagine crisp greens, roasted vegetables, nuts or seeds, a touch of cheese or a plant-based protein) paired with a side of whole-grain bread or an inventive grain bowl could serve as a kind of \u201cexplanatory synthesis\u201d for your body\u2019s needs. \n\nThis approach mirrors Deutsch\u2019s idea that progress is achieved by testing new ideas and being willing to depart from rote habits. Just as the growth of knowledge arises from conjecture and criticism, you can treat your meal as a small, personal experiment: try adding a new spice or ingredient you haven\u2019t used before, or mix elements of different cuisines.\n\nUltimately, the \u201cbest\u201d lunch is one that not only satisfies your immediate nutritional needs but also encourages you to think differently\u2014transforming a routine decision into a creative act. In other words, opt for a lunch that is both nourishing and innovative, one that supports your continual quest for knowledge and improvement. Enjoy your experiment!",
      "chunks": {
        "max_sim": "0.216",
        "max_stars": 5,
        "chunks": []
      },
      "large_context_filename": "deutsch_large_context_v1.md",
      "cost_pennies_mycalc": 1.09
    }
  }
}


## ====== schema_invalid_requests for qrag-llm ======

## schema_invalid_requests  Request 1: Exceeds maxLength
Original: {
  "description": "Exceeds maxLength",
  "request": {
    "metadata": {
      "timestamp": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    }
  }
}
Complete: {
  "description": "Exceeds maxLength",
  "request": {
    "metadata": {
      "timestamp": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
      "user_id": "default",
      "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
      "bot_version": "2.0",
      "routes_info": {
        "routes_flow_name": "3 routes, separate route prompts",
        "upper_sim_bound": 0.9,
        "lower_sim_bound": 0.3,
        "max_sim": "0.216",
        "max_stars": 5,
        "routes_dict_content": {
          "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
        }
      }
    },
    "content": {
      "user_question": "What should I eat for lunch?",
      "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
      "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
      "quoted_qa": "",
      "ai_answer": "WAITING FOR LLM RESPONSE",
      "chunks": {
        "max_sim": "0.216",
        "max_stars": 5,
        "chunks": []
      }
    }
  }
}

### DIRECT LAMBDA INVOCATION
Lambda response payload: {
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 200,
  "body": "{\"status\": \"Success\", \"response\": {\"metadata\": {\"timestamp\": \"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\", \"user_id\": \"default\", \"vector_index_name\": \"deutsch-transcript-qrag-83f-20250202\", \"bot_version\": \"2.0\", \"routes_info\": {\"routes_flow_name\": \"3 routes, separate route prompts\", \"upper_sim_bound\": 0.9, \"lower_sim_bound\": 0.3, \"max_sim\": \"0.216\", \"max_stars\": 5, \"routes_dict_content\": {\"routes_dict_name\": \"ROUTES_DICT_DEUTSCH_M1\"}}, \"llm_model\": \"o3-mini\"}, \"content\": {\"user_question\": \"What should I eat for lunch?\", \"route_preamble\": \"Your question is not addressed in David Deutsch's interviews.\", \"prompt_initial\": \"Given your knowledge of David Deutsch and his philosophy...\", \"quoted_qa\": \"\", \"ai_answer\": \"Drawing inspiration from David Deutsch\\u2019s approach to rational problem-solving and his emphasis on seeking the best explanations, you might treat your lunch decision as a small experiment in critical thinking. Deutsch would urge you to consider the evidence available\\u2014your hunger level, nutritional needs, available ingredients, and even your mood\\u2014and to choose a meal that contributes to both your immediate well-being and your long\\u2010term potential for creative, error\\u2010correcting progress.\\n\\nHere\\u2019s a way to apply that philosophy:\\n\\n1. Identify your objective clearly. Are you looking for fuel to power your afternoon\\u2019s work? Do you need a meal that\\u2019s both nutritious and light to keep your mind agile?\\n\\n2. Gather your \\u201cevidence.\\u201d Consider what ingredients you have available, whether you\\u2019re cooking or buying. Think about your nutritional goals (balanced protein, healthy fats, complex carbohydrates, fresh vegetables) as if they\\u2019re pieces of a theory that must work together harmoniously.\\n\\n3. Propose a hypothesis. For example, \\u201cA lunch that blends both tradition and innovation\\u2014say, a hearty salad with grilled chicken (or a protein of your choice), mixed greens, nuts, and a tangy dressing\\u2014will fuel my body and mind in a way that promotes clarity and optimism.\\u201d\\n\\n4. Critically test and refine. Reflect on past lunches. Did a similar meal boost your productivity? Did you feel balanced afterwards? Adjust based on that feedback.\\n\\nSo, if you\\u2019re looking for a concrete suggestion in the spirit of rational inquiry, you might consider:\\n\\n\\u2022 A well-balanced salad featuring mixed greens, a lean protein (like grilled chicken, tofu, or legumes), a mix of colorful vegetables, and a handful of nuts or seeds for healthy fat.  \\n\\u2022 Accompany it with a slice of whole-grain bread or a small serving of quinoa to incorporate some complex carbohydrates.  \\n\\u2022 Optionally, a side of fresh fruit to round out the meal with natural sweetness and additional nutrients.\\n\\nThis choice not only meets nutritional criteria but also reflects the kind of thoughtful decision-making process Deutsch encourages\\u2014a commitment to improving one\\u2019s situation based on the best available explanations and evidence.\\n\\nOf course, if you\\u2019re in a different mood or have a craving for something else, just apply the same critical approach. Examine your choices, consider how they align with your goals (whether those are health, enjoyment, or even sustainability), and select the option that best advances your well-being both practically and intellectually. Enjoy your lunch and the ongoing experiment of learning from every decision!\", \"chunks\": {\"max_sim\": \"0.216\", \"max_stars\": 5, \"chunks\": []}, \"cost_pennies_mycalc\": 0.539}}}"
}
Result:
{
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 200,
  "body": "{\"status\": \"Success\", \"response\": {\"metadata\": {\"timestamp\": \"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\", \"user_id\": \"default\", \"vector_index_name\": \"deutsch-transcript-qrag-83f-20250202\", \"bot_version\": \"2.0\", \"routes_info\": {\"routes_flow_name\": \"3 routes, separate route prompts\", \"upper_sim_bound\": 0.9, \"lower_sim_bound\": 0.3, \"max_sim\": \"0.216\", \"max_stars\": 5, \"routes_dict_content\": {\"routes_dict_name\": \"ROUTES_DICT_DEUTSCH_M1\"}}, \"llm_model\": \"o3-mini\"}, \"content\": {\"user_question\": \"What should I eat for lunch?\", \"route_preamble\": \"Your question is not addressed in David Deutsch's interviews.\", \"prompt_initial\": \"Given your knowledge of David Deutsch and his philosophy...\", \"quoted_qa\": \"\", \"ai_answer\": \"Drawing inspiration from David Deutsch\\u2019s approach to rational problem-solving and his emphasis on seeking the best explanations, you might treat your lunch decision as a small experiment in critical thinking. Deutsch would urge you to consider the evidence available\\u2014your hunger level, nutritional needs, available ingredients, and even your mood\\u2014and to choose a meal that contributes to both your immediate well-being and your long\\u2010term potential for creative, error\\u2010correcting progress.\\n\\nHere\\u2019s a way to apply that philosophy:\\n\\n1. Identify your objective clearly. Are you looking for fuel to power your afternoon\\u2019s work? Do you need a meal that\\u2019s both nutritious and light to keep your mind agile?\\n\\n2. Gather your \\u201cevidence.\\u201d Consider what ingredients you have available, whether you\\u2019re cooking or buying. Think about your nutritional goals (balanced protein, healthy fats, complex carbohydrates, fresh vegetables) as if they\\u2019re pieces of a theory that must work together harmoniously.\\n\\n3. Propose a hypothesis. For example, \\u201cA lunch that blends both tradition and innovation\\u2014say, a hearty salad with grilled chicken (or a protein of your choice), mixed greens, nuts, and a tangy dressing\\u2014will fuel my body and mind in a way that promotes clarity and optimism.\\u201d\\n\\n4. Critically test and refine. Reflect on past lunches. Did a similar meal boost your productivity? Did you feel balanced afterwards? Adjust based on that feedback.\\n\\nSo, if you\\u2019re looking for a concrete suggestion in the spirit of rational inquiry, you might consider:\\n\\n\\u2022 A well-balanced salad featuring mixed greens, a lean protein (like grilled chicken, tofu, or legumes), a mix of colorful vegetables, and a handful of nuts or seeds for healthy fat.  \\n\\u2022 Accompany it with a slice of whole-grain bread or a small serving of quinoa to incorporate some complex carbohydrates.  \\n\\u2022 Optionally, a side of fresh fruit to round out the meal with natural sweetness and additional nutrients.\\n\\nThis choice not only meets nutritional criteria but also reflects the kind of thoughtful decision-making process Deutsch encourages\\u2014a commitment to improving one\\u2019s situation based on the best available explanations and evidence.\\n\\nOf course, if you\\u2019re in a different mood or have a craving for something else, just apply the same critical approach. Examine your choices, consider how they align with your goals (whether those are health, enjoyment, or even sustainability), and select the option that best advances your well-being both practically and intellectually. Enjoy your lunch and the ongoing experiment of learning from every decision!\", \"chunks\": {\"max_sim\": \"0.216\", \"max_stars\": 5, \"chunks\": []}, \"cost_pennies_mycalc\": 0.539}}}"
}

### API GATEWAY INVOCATION
Request being sent to API Gateway:
{
  "metadata": {
    "timestamp": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "user_id": "default",
    "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
    "bot_version": "2.0",
    "routes_info": {
      "routes_flow_name": "3 routes, separate route prompts",
      "upper_sim_bound": 0.9,
      "lower_sim_bound": 0.3,
      "max_sim": "0.216",
      "max_stars": 5,
      "routes_dict_content": {
        "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
      }
    }
  },
  "content": {
    "user_question": "What should I eat for lunch?",
    "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
    "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
    "quoted_qa": "",
    "ai_answer": "WAITING FOR LLM RESPONSE",
    "chunks": {
      "max_sim": "0.216",
      "max_stars": 5,
      "chunks": []
    }
  }
}
Result:
{
  "message": "Invalid request body"
}

## schema_invalid_requests  Request 2: Empty required field
Original: {
  "description": "Empty required field",
  "request": {
    "content": {
      "user_question": ""
    }
  }
}
Complete: {
  "description": "Empty required field",
  "request": {
    "metadata": {
      "timestamp": "2024-06-13T11:46:33.651753",
      "user_id": "default",
      "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
      "bot_version": "2.0",
      "routes_info": {
        "routes_flow_name": "3 routes, separate route prompts",
        "upper_sim_bound": 0.9,
        "lower_sim_bound": 0.3,
        "max_sim": "0.216",
        "max_stars": 5,
        "routes_dict_content": {
          "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
        }
      }
    },
    "content": {
      "user_question": "",
      "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
      "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
      "quoted_qa": "",
      "ai_answer": "WAITING FOR LLM RESPONSE",
      "chunks": {
        "max_sim": "0.216",
        "max_stars": 5,
        "chunks": []
      }
    }
  }
}

### DIRECT LAMBDA INVOCATION
Lambda response payload: {
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 200,
  "body": "{\"status\": \"Success\", \"response\": {\"metadata\": {\"timestamp\": \"2024-06-13T11:46:33.651753\", \"user_id\": \"default\", \"vector_index_name\": \"deutsch-transcript-qrag-83f-20250202\", \"bot_version\": \"2.0\", \"routes_info\": {\"routes_flow_name\": \"3 routes, separate route prompts\", \"upper_sim_bound\": 0.9, \"lower_sim_bound\": 0.3, \"max_sim\": \"0.216\", \"max_stars\": 5, \"routes_dict_content\": {\"routes_dict_name\": \"ROUTES_DICT_DEUTSCH_M1\"}}, \"llm_model\": \"o3-mini\"}, \"content\": {\"user_question\": \"\", \"route_preamble\": \"Your question is not addressed in David Deutsch's interviews.\", \"prompt_initial\": \"Given your knowledge of David Deutsch and his philosophy...\", \"quoted_qa\": \"\", \"ai_answer\": \"Could you please clarify what specific aspect of David Deutsch or his philosophy you\\u2019d like to discuss? For example, are you interested in his ideas on quantum computation, his advocacy of the many\\u2010worlds interpretation, his views on epistemology as presented in The Fabric of Reality and The Beginning of Infinity, or something else? Let me know so I can provide the most relevant information.\", \"chunks\": {\"max_sim\": \"0.216\", \"max_stars\": 5, \"chunks\": []}, \"cost_pennies_mycalc\": 0.324}}}"
}
Result:
{
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 200,
  "body": "{\"status\": \"Success\", \"response\": {\"metadata\": {\"timestamp\": \"2024-06-13T11:46:33.651753\", \"user_id\": \"default\", \"vector_index_name\": \"deutsch-transcript-qrag-83f-20250202\", \"bot_version\": \"2.0\", \"routes_info\": {\"routes_flow_name\": \"3 routes, separate route prompts\", \"upper_sim_bound\": 0.9, \"lower_sim_bound\": 0.3, \"max_sim\": \"0.216\", \"max_stars\": 5, \"routes_dict_content\": {\"routes_dict_name\": \"ROUTES_DICT_DEUTSCH_M1\"}}, \"llm_model\": \"o3-mini\"}, \"content\": {\"user_question\": \"\", \"route_preamble\": \"Your question is not addressed in David Deutsch's interviews.\", \"prompt_initial\": \"Given your knowledge of David Deutsch and his philosophy...\", \"quoted_qa\": \"\", \"ai_answer\": \"Could you please clarify what specific aspect of David Deutsch or his philosophy you\\u2019d like to discuss? For example, are you interested in his ideas on quantum computation, his advocacy of the many\\u2010worlds interpretation, his views on epistemology as presented in The Fabric of Reality and The Beginning of Infinity, or something else? Let me know so I can provide the most relevant information.\", \"chunks\": {\"max_sim\": \"0.216\", \"max_stars\": 5, \"chunks\": []}, \"cost_pennies_mycalc\": 0.324}}}"
}

### API GATEWAY INVOCATION
Request being sent to API Gateway:
{
  "metadata": {
    "timestamp": "2024-06-13T11:46:33.651753",
    "user_id": "default",
    "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
    "bot_version": "2.0",
    "routes_info": {
      "routes_flow_name": "3 routes, separate route prompts",
      "upper_sim_bound": 0.9,
      "lower_sim_bound": 0.3,
      "max_sim": "0.216",
      "max_stars": 5,
      "routes_dict_content": {
        "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
      }
    }
  },
  "content": {
    "user_question": "",
    "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
    "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
    "quoted_qa": "",
    "ai_answer": "WAITING FOR LLM RESPONSE",
    "chunks": {
      "max_sim": "0.216",
      "max_stars": 5,
      "chunks": []
    }
  }
}
Result:
{
  "message": "Invalid request body"
}

## schema_invalid_requests  Request 3: Invalid data types in content
Original: {
  "description": "Invalid data types in content",
  "request": {
    "content": {
      "user_question": 12345
    }
  }
}
Complete: {
  "description": "Invalid data types in content",
  "request": {
    "metadata": {
      "timestamp": "2024-06-13T11:46:33.651753",
      "user_id": "default",
      "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
      "bot_version": "2.0",
      "routes_info": {
        "routes_flow_name": "3 routes, separate route prompts",
        "upper_sim_bound": 0.9,
        "lower_sim_bound": 0.3,
        "max_sim": "0.216",
        "max_stars": 5,
        "routes_dict_content": {
          "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
        }
      }
    },
    "content": {
      "user_question": 12345,
      "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
      "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
      "quoted_qa": "",
      "ai_answer": "WAITING FOR LLM RESPONSE",
      "chunks": {
        "max_sim": "0.216",
        "max_stars": 5,
        "chunks": []
      }
    }
  }
}

### DIRECT LAMBDA INVOCATION
Lambda response payload: {
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 200,
  "body": "{\"status\": \"Success\", \"response\": {\"metadata\": {\"timestamp\": \"2024-06-13T11:46:33.651753\", \"user_id\": \"default\", \"vector_index_name\": \"deutsch-transcript-qrag-83f-20250202\", \"bot_version\": \"2.0\", \"routes_info\": {\"routes_flow_name\": \"3 routes, separate route prompts\", \"upper_sim_bound\": 0.9, \"lower_sim_bound\": 0.3, \"max_sim\": \"0.216\", \"max_stars\": 5, \"routes_dict_content\": {\"routes_dict_name\": \"ROUTES_DICT_DEUTSCH_M1\"}}, \"llm_model\": \"o3-mini\"}, \"content\": {\"user_question\": 12345, \"route_preamble\": \"Your question is not addressed in David Deutsch's interviews.\", \"prompt_initial\": \"Given your knowledge of David Deutsch and his philosophy...\", \"quoted_qa\": \"\", \"ai_answer\": \"I notice that you mentioned David Deutsch and his philosophy, but the specific question (\\u201c12345\\u201d) isn\\u2019t entirely clear to me. Could you please clarify what you\\u2019d like to know? For example, are you interested in:\\n\\n\\u2022 Deutsch\\u2019s views on quantum mechanics and the multiverse?\\n\\u2022 His ideas about explanation, knowledge, and progress as discussed in works like The Fabric of Reality or The Beginning of Infinity?\\n\\u2022 How his philosophy connects to matters like optimism in science or the philosophy of objectivity?\\n\\nAny additional details you provide will help me give you a more focused and useful answer.\", \"chunks\": {\"max_sim\": \"0.216\", \"max_stars\": 5, \"chunks\": []}, \"cost_pennies_mycalc\": 0.37}}}"
}
Result:
{
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 200,
  "body": "{\"status\": \"Success\", \"response\": {\"metadata\": {\"timestamp\": \"2024-06-13T11:46:33.651753\", \"user_id\": \"default\", \"vector_index_name\": \"deutsch-transcript-qrag-83f-20250202\", \"bot_version\": \"2.0\", \"routes_info\": {\"routes_flow_name\": \"3 routes, separate route prompts\", \"upper_sim_bound\": 0.9, \"lower_sim_bound\": 0.3, \"max_sim\": \"0.216\", \"max_stars\": 5, \"routes_dict_content\": {\"routes_dict_name\": \"ROUTES_DICT_DEUTSCH_M1\"}}, \"llm_model\": \"o3-mini\"}, \"content\": {\"user_question\": 12345, \"route_preamble\": \"Your question is not addressed in David Deutsch's interviews.\", \"prompt_initial\": \"Given your knowledge of David Deutsch and his philosophy...\", \"quoted_qa\": \"\", \"ai_answer\": \"I notice that you mentioned David Deutsch and his philosophy, but the specific question (\\u201c12345\\u201d) isn\\u2019t entirely clear to me. Could you please clarify what you\\u2019d like to know? For example, are you interested in:\\n\\n\\u2022 Deutsch\\u2019s views on quantum mechanics and the multiverse?\\n\\u2022 His ideas about explanation, knowledge, and progress as discussed in works like The Fabric of Reality or The Beginning of Infinity?\\n\\u2022 How his philosophy connects to matters like optimism in science or the philosophy of objectivity?\\n\\nAny additional details you provide will help me give you a more focused and useful answer.\", \"chunks\": {\"max_sim\": \"0.216\", \"max_stars\": 5, \"chunks\": []}, \"cost_pennies_mycalc\": 0.37}}}"
}

### API GATEWAY INVOCATION
Request being sent to API Gateway:
{
  "metadata": {
    "timestamp": "2024-06-13T11:46:33.651753",
    "user_id": "default",
    "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
    "bot_version": "2.0",
    "routes_info": {
      "routes_flow_name": "3 routes, separate route prompts",
      "upper_sim_bound": 0.9,
      "lower_sim_bound": 0.3,
      "max_sim": "0.216",
      "max_stars": 5,
      "routes_dict_content": {
        "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
      }
    }
  },
  "content": {
    "user_question": 12345,
    "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
    "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
    "quoted_qa": "",
    "ai_answer": "WAITING FOR LLM RESPONSE",
    "chunks": {
      "max_sim": "0.216",
      "max_stars": 5,
      "chunks": []
    }
  }
}
Result:
{
  "message": "Invalid request body"
}


## ====== function_invalid_requests for qrag-llm ======

## function_invalid_requestsRequest 1: Missing required top-level field
Original: {
  "description": "Missing required top-level field",
  "request": {
    "metadata": "__REMOVE_FIELD__"
  }
}
Complete: {
  "description": "Missing required top-level field",
  "request": {
    "content": {
      "user_question": "What should I eat for lunch?",
      "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
      "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
      "quoted_qa": "",
      "ai_answer": "WAITING FOR LLM RESPONSE",
      "chunks": {
        "max_sim": "0.216",
        "max_stars": 5,
        "chunks": []
      }
    }
  }
}

### DIRECT LAMBDA INVOCATION
Lambda response payload: {
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 500,
  "body": "{\"error\": \"'metadata'\", \"error_type\": \"KeyError\", \"traceback\": \"Traceback (most recent call last):\\n  File \\\"/var/task/app.py\\\", line 72, in handle_qrag_llm\\n    received_request_data['metadata']['llm_model'] = SERVER_SIDE_LLM_MODEL\\n    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^\\nKeyError: 'metadata'\\n\"}"
}
Result:
{
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 500,
  "body": "{\"error\": \"'metadata'\", \"error_type\": \"KeyError\", \"traceback\": \"Traceback (most recent call last):\\n  File \\\"/var/task/app.py\\\", line 72, in handle_qrag_llm\\n    received_request_data['metadata']['llm_model'] = SERVER_SIDE_LLM_MODEL\\n    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^\\nKeyError: 'metadata'\\n\"}"
}

### API GATEWAY INVOCATION
Request being sent to API Gateway:
{
  "content": {
    "user_question": "What should I eat for lunch?",
    "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
    "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
    "quoted_qa": "",
    "ai_answer": "WAITING FOR LLM RESPONSE",
    "chunks": {
      "max_sim": "0.216",
      "max_stars": 5,
      "chunks": []
    }
  }
}
Result:
{
  "message": "Invalid request body"
}

## function_invalid_requestsRequest 2: Missing required content field
Original: {
  "description": "Missing required content field",
  "request": {
    "content": {
      "user_question": "__REMOVE_FIELD__"
    }
  }
}
Complete: {
  "description": "Missing required content field",
  "request": {
    "metadata": {
      "timestamp": "2024-06-13T11:46:33.651753",
      "user_id": "default",
      "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
      "bot_version": "2.0",
      "routes_info": {
        "routes_flow_name": "3 routes, separate route prompts",
        "upper_sim_bound": 0.9,
        "lower_sim_bound": 0.3,
        "max_sim": "0.216",
        "max_stars": 5,
        "routes_dict_content": {
          "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
        }
      }
    },
    "content": {
      "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
      "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
      "quoted_qa": "",
      "ai_answer": "WAITING FOR LLM RESPONSE",
      "chunks": {
        "max_sim": "0.216",
        "max_stars": 5,
        "chunks": []
      }
    }
  }
}

### DIRECT LAMBDA INVOCATION
Lambda response payload: {
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 500,
  "body": "{\"error\": \"Missing required fields in JSON object: user_question\", \"error_type\": \"ValueError\", \"traceback\": \"Traceback (most recent call last):\\n  File \\\"/var/task/app.py\\\", line 100, in handle_qrag_llm\\n    response_json_object = qrag_llm_call(\\n                           ^^^^^^^^^^^^^^\\n  File \\\"/var/task/chalicelib/rag.py\\\", line 398, in qrag_llm_call\\n    raise ValueError(f\\\"Missing required fields in JSON object: {', '.join(missing_fields)}\\\")\\nValueError: Missing required fields in JSON object: user_question\\n\"}"
}
Result:
{
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 500,
  "body": "{\"error\": \"Missing required fields in JSON object: user_question\", \"error_type\": \"ValueError\", \"traceback\": \"Traceback (most recent call last):\\n  File \\\"/var/task/app.py\\\", line 100, in handle_qrag_llm\\n    response_json_object = qrag_llm_call(\\n                           ^^^^^^^^^^^^^^\\n  File \\\"/var/task/chalicelib/rag.py\\\", line 398, in qrag_llm_call\\n    raise ValueError(f\\\"Missing required fields in JSON object: {', '.join(missing_fields)}\\\")\\nValueError: Missing required fields in JSON object: user_question\\n\"}"
}

### API GATEWAY INVOCATION
Request being sent to API Gateway:
{
  "metadata": {
    "timestamp": "2024-06-13T11:46:33.651753",
    "user_id": "default",
    "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
    "bot_version": "2.0",
    "routes_info": {
      "routes_flow_name": "3 routes, separate route prompts",
      "upper_sim_bound": 0.9,
      "lower_sim_bound": 0.3,
      "max_sim": "0.216",
      "max_stars": 5,
      "routes_dict_content": {
        "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
      }
    }
  },
  "content": {
    "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
    "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
    "quoted_qa": "",
    "ai_answer": "WAITING FOR LLM RESPONSE",
    "chunks": {
      "max_sim": "0.216",
      "max_stars": 5,
      "chunks": []
    }
  }
}
Result:
{
  "message": "Invalid request body"
}

## function_invalid_requestsRequest 3: Invalid data types in metadata
Original: {
  "description": "Invalid data types in metadata",
  "request": {
    "metadata": {
      "vector_index_name": [
        "invalid-type"
      ]
    }
  }
}
Complete: {
  "description": "Invalid data types in metadata",
  "request": {
    "metadata": {
      "timestamp": "2024-06-13T11:46:33.651753",
      "user_id": "default",
      "vector_index_name": [
        "invalid-type"
      ],
      "bot_version": "2.0",
      "routes_info": {
        "routes_flow_name": "3 routes, separate route prompts",
        "upper_sim_bound": 0.9,
        "lower_sim_bound": 0.3,
        "max_sim": "0.216",
        "max_stars": 5,
        "routes_dict_content": {
          "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
        }
      }
    },
    "content": {
      "user_question": "What should I eat for lunch?",
      "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
      "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
      "quoted_qa": "",
      "ai_answer": "WAITING FOR LLM RESPONSE",
      "chunks": {
        "max_sim": "0.216",
        "max_stars": 5,
        "chunks": []
      }
    }
  }
}

### DIRECT LAMBDA INVOCATION
Lambda response payload: {
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 500,
  "body": "{\"error\": \"'list' object has no attribute 'startswith'\", \"error_type\": \"AttributeError\", \"traceback\": \"Traceback (most recent call last):\\n  File \\\"/var/task/app.py\\\", line 118, in handle_qrag_llm\\n    if vector_index_name.startswith(\\\"deutsch\\\"):\\n       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^\\nAttributeError: 'list' object has no attribute 'startswith'\\n\"}"
}
Result:
{
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 500,
  "body": "{\"error\": \"'list' object has no attribute 'startswith'\", \"error_type\": \"AttributeError\", \"traceback\": \"Traceback (most recent call last):\\n  File \\\"/var/task/app.py\\\", line 118, in handle_qrag_llm\\n    if vector_index_name.startswith(\\\"deutsch\\\"):\\n       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^\\nAttributeError: 'list' object has no attribute 'startswith'\\n\"}"
}

### API GATEWAY INVOCATION
Request being sent to API Gateway:
{
  "metadata": {
    "timestamp": "2024-06-13T11:46:33.651753",
    "user_id": "default",
    "vector_index_name": [
      "invalid-type"
    ],
    "bot_version": "2.0",
    "routes_info": {
      "routes_flow_name": "3 routes, separate route prompts",
      "upper_sim_bound": 0.9,
      "lower_sim_bound": 0.3,
      "max_sim": "0.216",
      "max_stars": 5,
      "routes_dict_content": {
        "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
      }
    }
  },
  "content": {
    "user_question": "What should I eat for lunch?",
    "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
    "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
    "quoted_qa": "",
    "ai_answer": "WAITING FOR LLM RESPONSE",
    "chunks": {
      "max_sim": "0.216",
      "max_stars": 5,
      "chunks": []
    }
  }
}
Result:
{
  "message": "Invalid request body"
}

## function_invalid_requestsRequest 4: Large context filename not in S3 folder
Original: {
  "description": "Large context filename not in S3 folder",
  "request": {
    "metadata": {
      "large_context_filename": "not-present-filename.md"
    }
  }
}
Complete: {
  "description": "Large context filename not in S3 folder",
  "request": {
    "metadata": {
      "timestamp": "2024-06-13T11:46:33.651753",
      "user_id": "default",
      "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
      "bot_version": "2.0",
      "routes_info": {
        "routes_flow_name": "3 routes, separate route prompts",
        "upper_sim_bound": 0.9,
        "lower_sim_bound": 0.3,
        "max_sim": "0.216",
        "max_stars": 5,
        "routes_dict_content": {
          "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
        }
      },
      "large_context_filename": "not-present-filename.md"
    },
    "content": {
      "user_question": "What should I eat for lunch?",
      "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
      "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
      "quoted_qa": "",
      "ai_answer": "WAITING FOR LLM RESPONSE",
      "chunks": {
        "max_sim": "0.216",
        "max_stars": 5,
        "chunks": []
      }
    }
  }
}

### DIRECT LAMBDA INVOCATION
Lambda response payload: {
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 500,
  "body": "{\"error\": \"Failed to load required large context from not-present-filename.md\", \"error_type\": \"LargeContextLoadError\", \"vector_index\": \"deutsch-transcript-qrag-83f-20250202\"}"
}
Result:
{
  "headers": {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "https://www.focusonfoundations.org"
  },
  "multiValueHeaders": {},
  "statusCode": 500,
  "body": "{\"error\": \"Failed to load required large context from not-present-filename.md\", \"error_type\": \"LargeContextLoadError\", \"vector_index\": \"deutsch-transcript-qrag-83f-20250202\"}"
}

### API GATEWAY INVOCATION
Request being sent to API Gateway:
{
  "metadata": {
    "timestamp": "2024-06-13T11:46:33.651753",
    "user_id": "default",
    "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
    "bot_version": "2.0",
    "routes_info": {
      "routes_flow_name": "3 routes, separate route prompts",
      "upper_sim_bound": 0.9,
      "lower_sim_bound": 0.3,
      "max_sim": "0.216",
      "max_stars": 5,
      "routes_dict_content": {
        "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
      }
    },
    "large_context_filename": "not-present-filename.md"
  },
  "content": {
    "user_question": "What should I eat for lunch?",
    "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
    "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
    "quoted_qa": "",
    "ai_answer": "WAITING FOR LLM RESPONSE",
    "chunks": {
      "max_sim": "0.216",
      "max_stars": 5,
      "chunks": []
    }
  }
}
Result:
{
  "error": "Failed to load required large context from not-present-filename.md",
  "error_type": "LargeContextLoadError",
  "vector_index": "deutsch-transcript-qrag-83f-20250202"
}

## ===== API Gateway Validation Test Summary qrag-llm =====

clean_requests (2 tests):
  Lambda Results: (expected SUCCESS)  ✓
    test 1:  SUCCESS
    test 2:  SUCCESS
  Gateway Results: (expected SUCCESS)  ✓
    test 1:  SUCCESS
    test 2:  SUCCESS

schema_invalid_requests (3 tests):
  Lambda Results: (expected SUCCESS)  ✓
    test 1:  SUCCESS
    test 2:  SUCCESS
    test 3:  SUCCESS
  Gateway Results: (expected ERROR)  ✓
    test 1:  ERROR
    test 2:  ERROR
    test 3:  ERROR

function_invalid_requests (4 tests):
  Lambda Results: (expected ERROR)  ✓
    test 1:  ERROR
    test 2:  ERROR
    test 3:  ERROR
    test 4:  ERROR
  Gateway Results: (expected ERROR)  ✓
    test 1:  ERROR
    test 2:  ERROR
    test 3:  ERROR
    test 4:  ERROR

Test Results: 18 passed, 0 failed  ✓
