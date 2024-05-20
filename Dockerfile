FROM --platform=linux/arm64/v8 python:3.11.6-slim

RUN echo "deb http://deb.debian.org/debian bullseye main" > /etc/apt/sources.list \
    && echo "deb http://deb.debian.org/debian bullseye-updates main" >> /etc/apt/sources.list \
    && echo "deb http://security.debian.org/debian-security bullseye-security main" >> /etc/apt/sources.list

#update system і встановлення пакетів
RUN apt-get update -y \
    && pip install --upgrade pip \
    # Залежності для пайтон пакетів
    && pip install --upgrade setuptools \
    && apt-get install -y build-essential \
    # менеджер залежностей
    && pip install pipenv watchdog \
    # Прибираємо не потрібні файли
    && rm -rf /var/lib/apt/lists/* 

# RUN echo "Hello World" >> /hello.txt
# Встановолюємо залежності 
COPY ./Pipfile ./Pipfile.lock / 
# встановлює дев залежності парямо в систему
RUN pipenv sync --system

# створити і перейти в дерекоторію або просто перейти
WORKDIR /app
COPY ./ ./

EXPOSE 8000

# RUN python src/manage.py runserver


# CMD [ "sleep", "3", "&&", "python", "src/manage.py", "runserver" ]
ENTRYPOINT [ "python" ]
CMD ["src/manage.py", "runserver", "0.0.0.0:8000"]