#include <iostream>
#include <vector>
#include <random>
#include <thread>
#include <mutex>
#include <chrono>
#include <fstream>
#include <climits>
#include <algorithm>
using namespace std;

struct Edge {
    int vecino;
    int costo;
};

class DAG_PATH_FINDER {
public:
    vector<vector<Edge>> listaAdyacencia;
    vector<vector<int>> niveles;
    int mejoresCosto;
    vector<int> mejoresRuta;
    vector<pair<double, int>> HistorialCostos;
    mutex mtx;
    bool timeout;
    chrono::steady_clock::time_point start;

    DAG_PATH_FINDER() {
        generarDAG();
    }

    void generarDAG() {
        listaAdyacencia.resize(62);
        niveles.resize(13);
        niveles[0].push_back(0); // Nodo EIT

        int nodo = 1;
        for (int nivel = 1; nivel <= 12; ++nivel) {
            for (int i = 0; i < 5; ++i) {
                niveles[nivel].push_back(nodo++);
            }
        }

        random_device rd;
        mt19937 gen(rd());
        uniform_int_distribution<> dist(5, 20);

        for (int i = 0; i < 12; ++i) {
            for (int u : niveles[i]) {
                for (int v : niveles[i + 1]) {
                    int costo = dist(gen);
                    listaAdyacencia[u].push_back({v, costo});
                }
            }
        }
    }

    void BuscarRutaAleatoria() {
        random_device rd;
        mt19937 gen(rd());
    
        while (!timeout) {
            vector<int> ruta;
            int costoTotal = 0;
            int actual = 0;
            ruta.push_back(actual);
    
            for (int nivel = 1; nivel <= 12; ++nivel) {
                auto vecinos = listaAdyacencia[actual];
                if (vecinos.empty()) break;
    
                shuffle(vecinos.begin(), vecinos.end(), gen);
                const Edge& e = vecinos.front();
                costoTotal += e.costo;
                actual = e.vecino;
                ruta.push_back(actual);
            }
    
            if (any_of(niveles[12].begin(), niveles[12].end(), [&](int n) { return n == actual; })) {
                lock_guard<mutex> lock(mtx);
                if (costoTotal < mejoresCosto) {
                    mejoresCosto = costoTotal;
                    mejoresRuta = ruta;
                    auto now = chrono::steady_clock::now();
                    double segundos = chrono::duration<double>(now - start).count();
                    HistorialCostos.push_back({segundos, costoTotal});
                    cout << "Nuevo mejor costo encontrado: " << costoTotal << endl;
                    ofstream out("actual.csv");
                    for (int n : ruta) out << n << ",";
                    out << "\n";
                }

            }
        }
    }

    void EjecutarBusqueda(int K) {
        mejoresCosto = INT_MAX;
        mejoresRuta.clear();
        timeout = false;
        HistorialCostos.clear();
        start = chrono::steady_clock::now();

        vector<thread> threads;
        for (int i = 0; i < K; ++i) {
            threads.emplace_back(&DAG_PATH_FINDER::BuscarRutaAleatoria, this);
        }

        this_thread::sleep_for(chrono::seconds(60));
        timeout = true;
        for (auto& t : threads) t.join();

        lock_guard<mutex> lock(mtx);
        cout << "\n== Mejor ruta encontrada (Costo: " << mejoresCosto << ") ==" << endl;
        for (int n : mejoresRuta) cout << n << " ";
        cout << endl;

        ofstream out("costos.csv");
        out << "Tiempo,Costo\n";
        for (auto& p : HistorialCostos)
            out << p.first << "," << p.second << "\n";
        out.close();

    }
};

int main() {
    DAG_PATH_FINDER buscador;
    int K;
    cout << "Ingrese el número de threads a usar (1, 10, 20, 50, 100): ";
    cin >> K;
    buscador.EjecutarBusqueda(K);
    return 0;
}
