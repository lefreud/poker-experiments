#include <string>

class Node
{
public:
    Node(const std::string &p_informationSet);
    double *GetStrategy() const;
    double *GetAverageStrategy() const;
    void UpdateCumulativeStrategy(const double *p_strategy, double p_realizationWeight);
    void AccumulateActionRegrets(int p_actionIndex, double p_regret);
    std::string ToString() const;

private:
    std::string m_informationSet;
    double m_cumulativeStrategy[2];
    double m_cumulativeRegrets[2];
};