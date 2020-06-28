#include "node.h"
#include "constants.h"
#include <sstream>
#include <iomanip>

Node::Node(const std::string &p_informationSet) : m_informationSet(p_informationSet), m_cumulativeStrategy{0, 0}, m_cumulativeRegrets{0, 0}
{
}
double *Node::GetStrategy() const
{
    double normalizingSum = 0;
    for (std::size_t a = 0; a < NUM_ACTIONS; a++)
    {
        if (m_cumulativeRegrets[a] > 0)
        {
            normalizingSum += m_cumulativeRegrets[a];
        }
    }
    double *strategy = new double[NUM_ACTIONS];
    if (normalizingSum > 0)
    {
        for (std::size_t a = 0; a < NUM_ACTIONS; a++)
        {
            strategy[a] = m_cumulativeRegrets[a] > 0 ? m_cumulativeRegrets[a] / (double)normalizingSum : 0;
        }
    }
    else
    {
        for (std::size_t a = 0; a < NUM_ACTIONS; a++)
        {
            strategy[a] = 1 / (double)NUM_ACTIONS;
        }
    }
    return strategy;
}
double *Node::GetAverageStrategy() const
{
    double normalizingSum = 0;
    for (std::size_t a = 0; a < NUM_ACTIONS; a++)
    {
        normalizingSum += m_cumulativeStrategy[a];
    }
    double *averageStrategy = new double[NUM_ACTIONS];
    if (normalizingSum > 0)
    {
        for (std::size_t a = 0; a < NUM_ACTIONS; a++)
        {
            averageStrategy[a] = m_cumulativeStrategy[a] / (double)normalizingSum;
        }
    }
    else
    {
        for (std::size_t a = 0; a < NUM_ACTIONS; a++)
        {
            averageStrategy[a] = 1 / (double)NUM_ACTIONS;
        }
    }
    return averageStrategy;
}
void Node::UpdateCumulativeStrategy(const double *p_strategy, double p_realizationWeight)
{
    for (std::size_t a = 0; a < NUM_ACTIONS; a++)
    {
        m_cumulativeStrategy[a] += p_strategy[a] * p_realizationWeight;
    }
}
void Node::AccumulateActionRegrets(int p_actionIndex, double p_regret)
{
    m_cumulativeRegrets[p_actionIndex] += p_regret;
}
std::string Node::ToString() const
{
    std::ostringstream stream;
    double *averageStrategy = GetAverageStrategy();
    stream << m_informationSet << ":\t";
    for (std::size_t a = 0; a < NUM_ACTIONS; a++)
    {
        stream << ACTIONS[a] << ": " << std::fixed << std::setprecision(2) << averageStrategy[a] * 100 << " %\t";
    }
    delete[] averageStrategy;
    return stream.str();
}
