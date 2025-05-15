#include <algorithm>
#include <iostream>
#include <string>

class PojazdWodny {
 protected:
  std::string nazwa;
  int rok_produkcji;

 public:
  PojazdWodny(const std::string& nazwa, int rok_produkcji)
      : nazwa(nazwa), rok_produkcji(rok_produkcji) {}
  virtual ~PojazdWodny() = default;

  virtual void wypisz_info() const = 0;
  virtual void rozladunek() = 0;
  virtual void zaladunek() = 0;

  virtual int getCzasWplyniecia() const = 0;
  virtual int getCzasCumowania() const = 0;
  virtual int getCzasOdcumowania() const = 0;
  virtual int getCzasOdpyniecia() const = 0;
};

class Statek : public PojazdWodny {
 private:
  double ladownosc;

 public:
  Statek(const std::string& nazwa, int rok_produkcji, double ladownosc)
      : PojazdWodny(nazwa, rok_produkcji), ladownosc(ladownosc) {}

  void wypisz_info() const override {
    std::cout << "Statek: " << nazwa << ", rok produkcji: " << rok_produkcji
              << ", ladownosc: " << ladownosc << " ton\n";
  }
  void rozladunek() override {
    std::cout << nazwa << ": Rozladowanie towaru.\n";
  }
  void zaladunek() override { std::cout << nazwa << ": Zaladowanie towaru.\n"; }
  int getCzasWplyniecia() const override { return 5; }
  int getCzasCumowania() const override { return 10; }
  int getCzasOdcumowania() const override { return 3; }
  int getCzasOdpyniecia() const override { return 5; }

  void sprzatajPoklad() { std::cout << nazwa << ": Sprzatanie pokladu.\n"; }
};

class LodzPodwodna : public PojazdWodny {
 private:
  double max_glebokosc;

 public:
  LodzPodwodna(const std::string& nazwa, int rok_produkcji,
               double max_glebokosc)
      : PojazdWodny(nazwa, rok_produkcji), max_glebokosc(max_glebokosc) {}

  void wypisz_info() const override {
    std::cout << "Lodz Podwodna: " << nazwa
              << ", rok produkcji: " << rok_produkcji
              << ", maksymalna glebokosc: " << max_glebokosc << " m\n";
  }
  void rozladunek() override {
    std::cout << nazwa << ": Rozladowanie ladunku.\n";
  }
  void zaladunek() override {
    std::cout << nazwa << ": Zaladowanie ladunku.\n";
  }
  int getCzasWplyniecia() const override { return 8; }
  int getCzasCumowania() const override { return 12; }
  int getCzasOdcumowania() const override { return 4; }
  int getCzasOdpyniecia() const override { return 6; }

  void zanurz() {
    std::cout << nazwa << ": Zanurzanie do glebokosci " << max_glebokosc
              << " m.\n";
  }
};

class Zaglowiec : public PojazdWodny {
 private:
  double powierzchnia_zagli;

 public:
  Zaglowiec(const std::string& nazwa, int rok_produkcji,
            double powierzchnia_zagli)
      : PojazdWodny(nazwa, rok_produkcji),
        powierzchnia_zagli(powierzchnia_zagli) {}

  void wypisz_info() const override {
    std::cout << "Zaglowiec: " << nazwa << ", rok produkcji: " << rok_produkcji
              << ", powierzchnia zagli: " << powierzchnia_zagli << " m^2\n";
  }
  void rozladunek() override {
    std::cout << nazwa << ": Rozladowanie ladunku.\n";
  }
  void zaladunek() override {
    std::cout << nazwa << ": Zaladowanie ladunku.\n";
  }
  int getCzasWplyniecia() const override { return 6; }
  int getCzasCumowania() const override { return 9; }
  int getCzasOdcumowania() const override { return 3; }
  int getCzasOdpyniecia() const override { return 5; }

  void rozwinZagle() { std::cout << nazwa << ": Rozwija zagle.\n"; }
};

enum class Licencja { Statek, LodzPodwodna, Zaglowiec };

class Kapitan {
 private:
  std::string imie;
  std::string nazwisko;
  Licencja licencja;

 public:
  Kapitan(const std::string& imie, const std::string& nazwisko,
          Licencja licencja)
      : imie(imie), nazwisko(nazwisko), licencja(licencja) {}

  void prowadz(PojazdWodny& poj) {
    bool uprawnienia = false;
    switch (licencja) {
      case Licencja::Statek:
        if (dynamic_cast<Statek*>(&poj)) uprawnienia = true;
        break;
      case Licencja::LodzPodwodna:
        if (dynamic_cast<LodzPodwodna*>(&poj)) uprawnienia = true;
        break;
      case Licencja::Zaglowiec:
        if (dynamic_cast<Zaglowiec*>(&poj)) uprawnienia = true;
        break;
    }
    if (uprawnienia) {
      std::cout << "Kapitan " << imie << " " << nazwisko << " prowadzi: ";
      poj.wypisz_info();
    } else {
      std::cout << "Kapitan " << imie << " " << nazwisko
                << " nie ma licencji na ten typ pojazdu.\n";
    }
  }
};

class Port {
 private:
  int czas_w_porcie;

 public:
  Port() : czas_w_porcie(0) {}

  void przyjmij_pojazd(PojazdWodny* poj) {
    czas_w_porcie += poj->getCzasWplyniecia();
    std::cout << "[" << czas_w_porcie << "] Pojazd wplywa do portu.\n";
    czas_w_porcie += poj->getCzasCumowania();
    std::cout << "[" << czas_w_porcie << "] Pojazd zacumowany.\n";
    poj->zaladunek();
    poj->rozladunek();
  }

  void wypusc_pojazd(PojazdWodny* poj) {
    czas_w_porcie += poj->getCzasOdcumowania();
    std::cout << "[" << czas_w_porcie << "] Pojazd odcumowany.\n";
    czas_w_porcie += poj->getCzasOdpyniecia();
    std::cout << "[" << czas_w_porcie << "] Pojazd odpływa z portu.\n";
  }
};

int main() {
  Statek statek("HMS Test", 2020, 39000);
  LodzPodwodna lodz("U-boot", 1941, 300.0);
  Zaglowiec zaglowiec("USS Test", 1999, 200.0);

  Kapitan jacek("Jacek", "Wróbel", Licencja::Zaglowiec);
  Kapitan ferdynand("Ferdynand", "Kiepski", Licencja::LodzPodwodna);
  Kapitan adam("Adam", "Małysz", Licencja::Statek);

  statek.wypisz_info();
  lodz.wypisz_info();
  zaglowiec.wypisz_info();

  statek.sprzatajPoklad();
  lodz.zanurz();
  zaglowiec.rozwinZagle();

  jacek.prowadz(zaglowiec);
  ferdynand.prowadz(lodz);
  adam.prowadz(statek);

  Port port;
  std::cout << "-- Operacje portowe --\n";
  port.przyjmij_pojazd(&statek);
  port.wypusc_pojazd(&statek);
  port.przyjmij_pojazd(&lodz);
  port.wypusc_pojazd(&lodz);
  port.przyjmij_pojazd(&zaglowiec);
  port.wypusc_pojazd(&zaglowiec);

  return 0;
}